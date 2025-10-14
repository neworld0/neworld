# neworld/views/weeklybible_views.py  (REPLACE WHOLE FILE)

from __future__ import annotations

import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.safestring import mark_safe
from requests.adapters import HTTPAdapter

try:
    from urllib3.util.retry import Retry  # 권장 경로
except Exception:
    from requests.packages.urllib3.util.retry import Retry  # type: ignore

logger = logging.getLogger("neworld")

# 실제 소스에 맞게 필요 시 수정
WEEKLYBIBLE_SOURCE_URL = "https://wol.jw.org/ko/wol/meetings/r8/lp-ko"
WEEKLYBIBLE_ITEM_SELECTOR = "article"  # 부정확해도 폴백 로직이 작동

# ----- HTTP 세션 (재시도/백오프) -----


def _build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "HEAD"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (compatible; WeeklyBibleBot/1.0; +https://neworld.kr)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
    )
    return session


SESSION = _build_session()


def _safe_text(node, default: str = "") -> str:
    return node.get_text(strip=True) if node else default


# ----- 목록 파서 -----
def fetch_weeklybible_latest_data(
    url: str,
    item_selector: Optional[str] = None,
    limit: int = 20,
) -> List[Dict[str, Optional[str]]]:
    """
    주간 성경 연구 목록 파싱.
    반환: [{ 'week': str, 'link': str|None, 'summary': str }]
    """
    try:
        resp = SESSION.get(url, timeout=12)
        status = resp.status_code
        text = resp.text or ""
    except Exception as e:
        logger.error(f"[weeklybible] 요청 실패: {e}")
        return []

    # 보호/차단 징후가 있어도 폴백 계속 시도
    if status >= 400 or len(text) < 800 or ("captcha" in text.lower()) or ("request blocked" in text.lower()):
        logger.warning(
            f"[weeklybible] 비정상 응답 감지(status={status}, len={len(text)}). 폴백 진행.")

    soup = BeautifulSoup(text, "html.parser")

    # 1차: 지정 selector → 일반 후보군
    items = soup.select(item_selector) if item_selector else []
    if not items:
        for cand in ["article", "li", "div.post", ".card", ".list-item", ".result-item", "section", ".entry"]:
            items = soup.select(cand)
            if items:
                logger.info(
                    f"[weeklybible] selector 대체 사용: {cand} (count={len(items)})")
                break

    results: List[Dict[str, Optional[str]]] = []

    def _push_result(title_node, container) -> bool:
        title = _safe_text(title_node)
        if not title:
            return False
        a = title_node if getattr(
            title_node, "name", "") == "a" else title_node.find("a")
        if not a and container:
            a = container.find("a")
        href = a["href"] if a and a.has_attr("href") else None
        abs_link = urljoin(url, href) if href else None
        summary_node = None
        if container:
            summary_node = container.find("p") or container.select_one(
                ".summary, .desc, .excerpt, .card-text")
        summary = _safe_text(summary_node)
        results.append({"week": title, "link": abs_link, "summary": summary})
        return True

    # 1차 파싱 (헤더 없으면 항목 스킵)
    if items:
        for idx, item in enumerate(items):
            try:
                head = (
                    item.find("h1")
                    or item.find("h2")
                    or item.select_one("header h1, header h2, .title, .post-title, .card-title, a[title]")
                )
                if not head:
                    logger.info(f"[weeklybible] item#{idx}: 제목 헤더 없음 → 스킵")
                    continue
                if _push_result(head, item) and len(results) >= limit:
                    break
            except Exception as e:
                logger.warning(f"[weeklybible] item#{idx} 파싱 실패: {e}")
                continue

    # 2차 폴백: 전역 링크 스캔(키워드)
    if len(results) < max(1, min(5, limit)):
        keywords = ("meeting", "meetings", "workbook",
                    "주간", "주일", "집회", "연구", "모임")
        anchors = soup.select("a[href]")
        picked = 0
        for a in anchors:
            try:
                txt = _safe_text(a)
                href = a.get("href")
                if not txt or not href:
                    continue
                blob = (txt + " " + href).lower()
                if any(k in blob for k in keywords):
                    container = a.find_parent(
                        ["article", "li", "div", "section"])
                    _push_result(a, container)
                    picked += 1
                    if len(results) >= limit or picked >= 10:
                        break
            except Exception:
                continue
        if picked:
            logger.info(f"[weeklybible] 전역 링크 스캔 폴백으로 {picked}건 확보")

    if not results:
        logger.warning(
            "[weeklybible] 결과 0건. 선택자/URL 점검 또는 보호 페이지(캡차) 가능성 확인 필요.")
    return results


# ----- 상세 파서 -----
def fetch_weeklybible_detail(url: str) -> Dict[str, str]:
    """
    상세 페이지 파싱.
    반환: { 'title': str, 'content_html': str(HTML), 'source_url': str }
    """
    try:
        resp = SESSION.get(url, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"[weeklybible-detail] 요청 실패: {e}")
        return {
            "title": "",
            "content_html": "<p>상세 페이지를 불러오지 못했습니다.</p>",
            "source_url": url,
        }

    soup = BeautifulSoup(resp.text, "html.parser")

    head = soup.find("h1") or soup.find("h2") or soup.select_one(
        "header h1, header h2, .title, .post-title")
    title = _safe_text(head, default="")

    content = (
        soup.select_one("article")
        or soup.select_one("main article")
        or soup.select_one("#content")
        or soup.select_one(".content, .article-body, .post-content, .entry-content")
    )
    if not content:
        paras = soup.select("article p") or soup.select("p")
        html = "".join(str(p)
                       for p in paras[:20]) if paras else "<p>표시할 내용이 없습니다.</p>"
    else:
        html = str(content)

    return {"title": title, "content_html": html, "source_url": url}


# ----- 뷰 -----
@login_required
def weeklybible(request):
    """
    목록 페이지: /neworld/weeklybible/
    템플릿: templates/neworld/weeklybible.html
    컨텍스트: items, source_url, empty_reason(옵션)
    """
    url = WEEKLYBIBLE_SOURCE_URL
    selector = WEEKLYBIBLE_ITEM_SELECTOR
    items = fetch_weeklybible_latest_data(url, selector, limit=20)

    context = {"items": items, "source_url": url}
    if not items:
        context["empty_reason"] = (
            "목록을 찾지 못했습니다. 사이트 구조 변경 또는 접근 차단(캡차)일 수 있습니다. "
            "잠시 후 새로고침하거나, 원문 페이지에서 직접 확인해 주세요."
        )
    return render(request, "neworld/weeklybible.html", context)


@login_required
def weeklybible_detail(request, *args, **kwargs):
    """
    상세 페이지: /neworld/weeklybible/<...> 또는 ?url= 로 접근
    """
    link = kwargs.get("url") or kwargs.get("link") or request.GET.get("url")
    if not link:
        return HttpResponseBadRequest("상세 페이지 URL이 제공되지 않았습니다.")
    data = fetch_weeklybible_detail(link)
    context = {
        "title": data.get("title") or "상세 보기",
        "content_html": mark_safe(data.get("content_html", "")),
        "source_url": data.get("source_url", link),
    }
    return render(request, "neworld/weeklybible_detail.html", context)
