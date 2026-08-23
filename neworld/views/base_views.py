import datetime
import logging
from pathlib import Path

from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache

from neworld.models import Scripture
from neworld.services.crawler import persist_scripture
from neworld.services.scripture_parser import parse_monthly_scriptures

from neworld.services.wol_client import WolClientError
logger = logging.getLogger("neworld")


def prefetch_future_scriptures(today):
    """Import a browser-saved monthly document when today's row is current."""
    directory = Path(getattr(settings, "SCRIPTURE_MONTHLY_HTML_DIR", settings.BASE_DIR / "data" / "scripture_html"))
    html_path = directory / ("%04d-%02d.html" % (today.year, today.month))
    if not html_path.is_file():
        logger.info("event=LOCAL_SCRIPTURE_HTML_MISSING path=%s", html_path)
        return
    cache_key = "scripture-import:local-html:v1:%s:%s" % (today.isoformat(), html_path.stat().st_mtime_ns)
    if not cache.add(cache_key, True, timeout=900):
        return
    try:
        raw = html_path.read_bytes()
        html = None
        for encoding in ("utf-8-sig", "utf-8", "cp949"):
            try:
                html = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                pass
        if not html:
            raise ValueError("Unsupported saved HTML encoding")
        items = parse_monthly_scriptures(html, today.year, today.month, html_path.resolve().as_uri())
    except (OSError, ValueError, WolClientError) as exc:
        logger.warning("event=LOCAL_SCRIPTURE_HTML_FAIL path=%s reason=%s", html_path, exc.__class__.__name__)
        return
    counts = {"inserted": 0, "skipped": 0}
    for item in items:
        counts[persist_scripture(item)] += 1
    logger.info("event=LOCAL_SCRIPTURE_HTML_SUMMARY path=%s parsed=%s inserted=%s skipped=%s", html_path, len(items), counts["inserted"], counts["skipped"])

def index(request):
    """Render saved Scripture and prefetch a week once today's row is current."""
    today_date = datetime.date.today()
    today = today_date.isoformat()
    valid_rows = Scripture.objects.exclude(scripture="").exclude(bodytext="").exclude(
        scripture__iexact="데이터 준비 중").exclude(bodytext__iexact="데이터 준비 중")
    today_rows = valid_rows.filter(real_date=today).order_by("id")
    latest = valid_rows.order_by("-real_date", "-id").first()
    if latest and latest.real_date == today:
        prefetch_future_scriptures(today_date)
    duplicate_count = today_rows.count()
    if duplicate_count > 1:
        logger.warning("event=SCRIPTURE_DUPLICATE_DATE target_date=%s candidate_count=%s", today, duplicate_count)
    scripture = today_rows.first()
    is_fallback = False
    if scripture is None:
        scripture = valid_rows.filter(real_date__lte=today).order_by("-real_date", "id").first()
        is_fallback = scripture is not None
        logger.warning("event=SCRIPTURE_VIEW_FALLBACK target_date=%s status=%s", today, "historical" if scripture else "empty")
    return render(request, "neworld/index.html", {
        "today_html": scripture.real_date if scripture else today,
        "day_of_week_html": scripture.d_week if scripture else "",
        "scripture_html": scripture.scripture if scripture else "",
        "bodyText_html": scripture.bodytext if scripture else "",
        "scripture_is_fallback": is_fallback,
        "scripture_is_empty": scripture is None,
    })
