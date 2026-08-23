import datetime
import logging

from django.core.management.base import BaseCommand, CommandError

from neworld.services.crawler import persist_weeklybible
from neworld.services.weeklybible_parser import next_iso_week, parse_weeklybible
from neworld.services.wol_client import WolClient, WolClientError

logger = logging.getLogger("neworld.crawler")


class Command(BaseCommand):
    help = "Fetch and validate one WeeklyBible record outside request handling."

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int)
        parser.add_argument("--week", type=int)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        if bool(options["year"]) != bool(options["week"]):
            raise CommandError("--year and --week must be supplied together")
        year, week = (options["year"], options["week"]) if options["year"] else next_iso_week(datetime.date.today())
        try:
            datetime.date.fromisocalendar(year, week, 1)
        except ValueError as exc:
            raise CommandError("Invalid ISO year/week") from exc
        url = "https://wol.jw.org/ko/wol/meetings/r8/lp-ko/%s/%s" % (year, week)
        try:
            response = WolClient().get_html(url)
            item = parse_weeklybible(response.text, year, week, response.url)
            logger.info("event=WOL_PARSE_OK source=weeklybible target_year=%s target_week=%s candidate_count=1", year, week)
            result = persist_weeklybible(item, options["dry_run"])
        except WolClientError as exc:
            logger.warning("event=WOL_PARSE_FAIL source=weeklybible target_year=%s target_week=%s reason=%s", year, week, exc.__class__.__name__)
            raise CommandError(str(exc))
        logger.info("event=CRAWLER_COMMAND_SUMMARY source=weeklybible inserted=%s skipped=%s", int(result == "inserted"), int(result == "skipped"))
        self.stdout.write("inserted=%s skipped=%s dry_run=%s" % (int(result == "inserted"), int(result == "skipped"), options["dry_run"]))
