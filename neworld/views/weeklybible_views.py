# neworld/views/weeklybible_views.py  (REPLACE WHOLE FILE)

from __future__ import annotations

import datetime
import logging
from typing import List, Dict, Optional
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.utils.safestring import mark_safe
from requests.adapters import HTTPAdapter

from neworld.models import WeeklyBible

try:
    from urllib3.util.retry import Retry  # 권장 경로
except Exception:
    from requests.packages.urllib3.util.retry import Retry  # type: ignore

logger = logging.getLogger("neworld")


# ======= 설정 (필요 시 실제 목록 페이지/선택자로 조정) =======
WEEKLYBIBLE_SOURCE_URL = "https://wol.jw.org/ko/wol/d/r8/lp-ko"
# 컨테이너 선택자: 부정확해도 아래 폴백이 작동
WEEKLYBIBLE_ITEM_SELECTOR = "article"

# ======= HTTP 세션: 재시도/백오프/헤더 =======


def _build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.6,  # 0.6s, 1.2s, 2.4s ...
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
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.6",
        }
    )
    return session


SESSION = _build_session()


# ======= 유틸 =======
def _safe_text(node, default: str = "") -> str:
    return node.get_text(strip=True) if node else default


def _guess_year_and_next_week() -> tuple[int, int]:
    """
    프로젝트에 target_year/target_next_week 계산이 없을 때를 대비한 보정값.
    (Asia/Seoul 기준 '다음 주' 주차)
    """
    today = timezone.localdate()
    # ISO 주차(월요일 시작). 일요일 문화면 필요시 조정 가능.
    iso_year, iso_week, _iso_wday = today.isocalendar()
    # '다음 주' 기준
    next_week = iso_week + 1
    year_val = iso_year
    # 연말/연초 경계 보정
    if next_week > 52:
        # ISO week 53 고려
        if datetime.date(iso_year, 12, 28).isocalendar()[1] == 53 and next_week == 54:
            # 드물지만 53주인 해에서 +1 했을 때 54가 되지 않도록
            next_week = 1
            year_val = iso_year + 1
        elif next_week == 53 and datetime.date(iso_year, 12, 28).isocalendar()[1] == 52:
            next_week = 1
            year_val = iso_year + 1
        elif next_week == 53:
            # 53주 존재
            pass
    return year_val, next_week


def _extract_specific_id_from_path(path: str) -> str:
    """
    기존 코드에서 /r8/lp-ko/202021321/ 처럼 '뒤에서 3번째 토큰'을 쓰던 패턴을 최대한 호환.
    안전하게: 토큰이 3개 이상이면 -3, 아니면 마지막 토큰 사용.
    """
    tokens = [t for t in path.split("/") if t]
    if len(tokens) >= 3:
        return tokens[-3]
    return tokens[-1] if tokens else ""


# ======= 목록 파서 (WeeklyBible 스키마에 맞춰 dict 반환) =======
def fetch_weeklybible_latest_data(url: str, item_selector: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """
    최신(들) 주간 성경 연구 항목을 파싱하여 WeeklyBible 스키마에 맞는 dict 리스트로 반환.
    스키마: {'year','n_week','week','bible_range','bible_link','specific_id','create_date'}
    방어적 파싱(다중 선택자·전역 키워드 스캔) + 상대경로 절대화 포함.
    """
    try:
        resp = SESSION.get(url, timeout=12)
        status = resp.status_code
        text = resp.text or ""
    except Exception as e:
        logger.error(f"[weeklybible] 요청 실패: {e}")
        return []

    # 보호/차단 시도 흔적이 있어도 폴백 탐색은 진행
    if status >= 400 or len(text) < 600 or ("captcha" in text.lower()) or ("request blocked" in text.lower()):
        logger.warning(
            f"[weeklybible] 비정상 응답 감지(status={status}, len={len(text)}). 폴백 탐색 수행.")

    soup = BeautifulSoup(text, "html.parser")

    # 1차: 지정 선택자
    items = soup.select(item_selector) if item_selector else []

    # 2차: 일반적인 컨테이너 후보군
    if not items:
        for cand in [
            "article", "section", "li", "div.post", ".card",
            ".list-item", ".result-item", ".entry", ".media",
            "ul li", ".cards .card", ".teaser",
        ]:
            items = soup.select(cand)
            if items:
                logger.info(
                    f"[weeklybible] selector 대체 사용: {cand} (count={len(items)})")
                break

    results: List[Dict] = []
    year_val, nweek_val = _guess_year_and_next_week()

    def _push_from_container(container) -> bool:
        # 제목 헤더: h1→h2→h3→공통 타이틀 후보
        head = (
            container.find("h1")
            or container.find("h2")
            or container.find("h3")
            or container.select_one("header h1, header h2, header h3, .title, .post-title, .card-title, .entry-title, a[title]")
        )
        if not head:
            return False

        week_title = _safe_text(head)
        if not week_title:
            return False

        # 범위/부제 후보
        sub = container.find("h2") or container.find("h3") or container.find(
            "p") or container.select_one(".summary, .desc, .excerpt, .card-text")
        bible_range = _safe_text(sub)

        # 링크
        a = head if getattr(head, "name", "") == "a" else head.find("a")
        if not a:
            a = container.find("a")
        href = a["href"] if a and a.has_attr("href") else None

        bible_link = ""
        specific_id = ""
        if href:
            abs_link = urljoin(url, href)
            parts = urlparse(abs_link)
            bible_link = f"{parts.scheme}://{parts.netloc}{parts.path}"
            specific_id = _extract_specific_id_from_path(parts.path)

        results.append(
            {
                "year": year_val,
                "n_week": nweek_val,
                "week": week_title,
                "bible_range": bible_range,
                "bible_link": bible_link,
                "specific_id": specific_id,
                "create_date": timezone.now(),
            }
        )
        return True

    # 1차: 컨테이너 기반 파싱
    if items:
        for idx, it in enumerate(items):
            try:
                if _push_from_container(it) and len(results) >= limit:
                    break
            except Exception as e:
                logger.warning(f"[weeklybible] item#{idx} 파싱 실패: {e}")
                continue

    # 2차 폴백: 전역 링크 스캔(키워드)
    if len(results) < max(1, min(5, limit)):
        anchors = soup.select("a[href]")
        keywords = ("meeting", "meetings", "workbook",
                    "주간", "주일", "집회", "연구", "모임")
        picked = 0
        for a in anchors:
            try:
                txt = _safe_text(a)
                href = a.get("href")
                if not txt or not href:
                    continue
                blob = (txt + " " + href).lower()
                if any(k in blob for k in keywords):
                    # 주변 컨테이너를 찾아 요약 텍스트 후보로 활용
                    container = a.find_parent(
                        ["article", "section", "li", "div"])
                    # 컨테이너가 없어도 최소 필드로 넣기
                    bible_link = ""
                    specific_id = ""
                    abs_link = urljoin(url, href)
                    parts = urlparse(abs_link)
                    if parts.scheme and parts.netloc:
                        bible_link = f"{parts.scheme}://{parts.netloc}{parts.path}"
                        specific_id = _extract_specific_id_from_path(
                            parts.path)
                    summary = ""
                    if container:
                        sub = container.find("p") or container.select_one(
                            ".summary, .desc, .excerpt, .card-text")
                        summary = _safe_text(sub)

                    results.append(
                        {
                            "year": year_val,
                            "n_week": nweek_val,
                            "week": txt,
                            "bible_range": summary,
                            "bible_link": bible_link,
                            "specific_id": specific_id,
                            "create_date": timezone.now(),
                        }
                    )
                    picked += 1
                    if len(results) >= limit or picked >= 10:
                        break
            except Exception:
                continue
        if picked:
            logger.info(f"[weeklybible] 전역 링크 스캔 폴백으로 {picked}건 확보")

    if not results:
        logger.warning("[weeklybible] 결과 0건. 선택자/URL 점검 또는 보호(캡차) 가능성 확인 필요.")
    return results


# ======= 상세 파서 (상세 페이지가 필요할 경우) =======
def fetch_weeklybible_detail(url: str) -> Dict[str, str]:
    """
    상세 페이지 파싱. (필수는 아님 — 외부로 이동만 해도 됨)
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


# ======= 목록 뷰: DB 우선 표시 + 신건만 삽입 =======
@login_required
def weeklybible(request):
    """
    /neworld/weeklybible/
    1) 먼저 DB에서 과거 데이터 표시 (네트워크 실패 대비)
    2) 일정 주기(기본 6시간)로 원격 갱신 시도하여 DB upsert
    """
    url = WEEKLYBIBLE_SOURCE_URL
    selector = WEEKLYBIBLE_ITEM_SELECTOR

    # --- 1) 화면 우선용 캐시(과거 데이터) ---
    cached_qs = WeeklyBible.objects.all().order_by("-create_date")
    cached_items = list(cached_qs[:20])

    # --- 2) 과도한 원격 트래픽 방지 — 6시간 내 갱신했으면 생략 ---
    needs_refresh = True
    if cached_items:
        latest_ts = cached_items[0].create_date
        needs_refresh = (timezone.now() -
                         latest_ts) > datetime.timedelta(hours=6)

    # --- 3) 원격 갱신 시도 & 신건만 삽입 ---
    if needs_refresh:
        fetched = fetch_weeklybible_latest_data(url, selector, limit=20)
        if fetched:
            # 마지막 저장 specific_id
            last = cached_items[0] if cached_items else None
            last_sid = getattr(last, "specific_id", "") if last else ""
            to_insert = []
            for it in fetched:
                sid = it.get("specific_id") or ""
                # specific_id가 비어 있으면 중복 판정이 어렵기 때문에 그냥 추가(드문 케이스)
                if sid and sid == last_sid:
                    break
                to_insert.append(it)
            # 시간 순서대로 삽입
            to_insert.reverse()
            for it in to_insert:
                WeeklyBible.objects.create(
                    year=it["year"],
                    n_week=it["n_week"],
                    week=it["week"],
                    bible_range=it["bible_range"],
                    bible_link=it["bible_link"] or None,
                    specific_id=it["specific_id"],
                    create_date=it["create_date"],
                )
            # 반영된 최신 데이터 다시 로드
            cached_qs = WeeklyBible.objects.all().order_by("-create_date")
            cached_items = list(cached_qs[:20])

    # --- 4) 검색/정렬/페이지네이션 (기존 템플릿 호환) ---
    page = request.GET.get("page", "1")
    kw = request.GET.get("kw", "")
    so = request.GET.get("so", "recent")  # recent / week / year

    qs = WeeklyBible.objects.all()
    if kw:
        qs = qs.filter(Q(week__icontains=kw) | Q(bible_range__icontains=kw))

    if so == "week":
        qs = qs.order_by("-n_week", "-create_date")
    elif so == "year":
        qs = qs.order_by("-year", "-n_week")
    else:
        qs = qs.order_by("-create_date")

    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)

    # target_* 컨텍스트가 필요한 템플릿이 있을 수 있어 안전 제공
    year_val, nweek_val = _guess_year_and_next_week()

    context = {
        "weeklybible_list": page_obj,          # 기존 목록 템플릿 호환
        "target_week": nweek_val,              # (기존 템플릿에서 참조 가능성)
        "target_year": year_val,               # (기존 템플릿에서 참조 가능성)
        "page": page,
        "kw": kw,
        "so": so,
        # 새 템플릿(간단 카드형)을 위한 데이터도 병행 제공
        "items": [
            {"week": x.week, "link": x.bible_link or "", "summary": x.bible_range}
            for x in cached_items
        ],
        "source_url": url,
    }
    if not cached_items:
        context["empty_reason"] = (
            "목록을 찾지 못했습니다. 사이트 구조 변경 또는 접근 차단(캡차)일 수 있습니다. "
            "잠시 후 새로고침하거나, 원문 페이지에서 직접 확인해 주세요."
        )
    return render(request, "neworld/weeklybible.html", context)


# ======= 상세 뷰 (옵션) =======
@login_required
def weeklybible_detail(request, *args, **kwargs):
    """
    /neworld/weeklybible/detail/?url=<외부링크>
    또는 /neworld/weeklybible/<path:url>/ 라우팅도 지원 가능(urls.py에서 패턴만 맞추면 됨)
    """
    link = kwargs.get("url") or kwargs.get("link") or request.GET.get("url")
    if not link:
        return HttpResponseBadRequest("상세 페이지 URL이 제공되지 않았습니다.")

    data = fetch_weeklybible_detail(link)
    context = {
        "title": data.get("title") or "상세 보기",
        # 필요 시 sanitize
        "content_html": mark_safe(data.get("content_html", "")),
        "source_url": data.get("source_url", link),
    }
    return render(request, "neworld/weeklybible_detail.html", context)
