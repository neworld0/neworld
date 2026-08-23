import logging

from django.db import transaction

from neworld.lib import get_day_of_week
from neworld.models import Scripture, WeeklyBible

from .scripture_parser import PLACEHOLDERS

logger = logging.getLogger("neworld.crawler")


def _valid(value):
    return bool(value and value.strip() and value.strip().casefold() not in PLACEHOLDERS)


def persist_scripture(item, dry_run=False):
    if not _valid(item.scripture_text) or not _valid(item.body_text):
        logger.warning("event=SCRIPTURE_PERSIST_SKIP target_date=%s reason=invalid_payload", item.source_date)
        return "skipped"
    matches = Scripture.objects.filter(real_date=item.source_date.isoformat()).order_by("id")
    if matches.count() > 1:
        logger.warning("event=SCRIPTURE_DUPLICATE_DATE target_date=%s", item.source_date)
    existing = matches.filter(scripture=item.scripture_text, bodytext=item.body_text).first()
    if existing or dry_run:
        logger.info("event=SCRIPTURE_PERSIST_SKIP target_date=%s reason=%s", item.source_date, "exists" if existing else "dry_run")
        return "skipped"
    Scripture.objects.create(
        scripture=item.scripture_text, bodytext=item.body_text,
        real_date=item.source_date.isoformat(),
        d_week=get_day_of_week(item.source_date.year, item.source_date.month, item.source_date.day),
    )
    logger.info("event=SCRIPTURE_PERSIST_OK target_date=%s inserted=1", item.source_date)
    return "inserted"


@transaction.atomic
def persist_weeklybible(item, dry_run=False):
    valid = all(value and value.strip() for value in (item.week, item.bible_range, item.bible_link, item.specific_id))
    if not valid:
        logger.warning("event=WEEKLYBIBLE_PERSIST_SKIP target_year=%s target_week=%s reason=invalid_payload", item.year, item.n_week)
        return "skipped"
    exists = (WeeklyBible.objects.filter(specific_id=item.specific_id).exists() or
              WeeklyBible.objects.filter(year=item.year, n_week=item.n_week).exists())
    if exists or dry_run:
        logger.info("event=WEEKLYBIBLE_PERSIST_SKIP target_year=%s target_week=%s reason=%s", item.year, item.n_week, "exists" if exists else "dry_run")
        return "skipped"
    WeeklyBible.objects.create(year=item.year, n_week=item.n_week, week=item.week,
                               bible_range=item.bible_range, bible_link=item.bible_link,
                               specific_id=item.specific_id)
    logger.info("event=WEEKLYBIBLE_PERSIST_OK target_year=%s target_week=%s inserted=1", item.year, item.n_week)
    return "inserted"
