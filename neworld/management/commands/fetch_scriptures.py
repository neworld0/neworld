import datetime
import logging

from django.core.management.base import BaseCommand, CommandError

from neworld.services.crawler import persist_scripture
from neworld.services.scripture_parser import parse_scripture
from neworld.services.wol_client import WolClient, WolClientError
from neworld.models import Scripture

logger = logging.getLogger("neworld.crawler")


def default_collection_window(today):
    """Return the safe default start date and count for a command run."""
    latest = (Scripture.objects.exclude(scripture="").exclude(bodytext="")
              .exclude(scripture__iexact="??? ?? ?")
              .exclude(bodytext__iexact="??? ?? ?")
              .filter(real_date__lte=today.isoformat())
              .order_by("-real_date", "-id")
              .first())
    if latest and latest.real_date == today.isoformat():
        return today + datetime.timedelta(days=1), 7
    return today, 1


class Command(BaseCommand):
    help = "Fetch and validate daily Scripture outside request handling."

    def add_arguments(self, parser):
        parser.add_argument("--date", dest="target_date", type=datetime.date.fromisoformat)
        parser.add_argument("--days", type=int)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        if options["target_date"]:
            start = options["target_date"]
            days = options["days"] or 1
        else:
            start, default_days = default_collection_window(datetime.date.today())
            days = options["days"] or default_days
        if days < 1 or days > 31:
            raise CommandError("--days must be between 1 and 31")
        counts = {"inserted": 0, "skipped": 0}
        client = WolClient()
        try:
            for offset in range(days):
                target = start + datetime.timedelta(days=offset)
                url = "https://wol.jw.org/ko/wol/h/r8/lp-ko/%s" % target.strftime("%Y/%m/%d")
                response = client.get_html(url)
                item = parse_scripture(response.text, target, response.url)
                logger.info("event=WOL_PARSE_OK source=scripture target_date=%s candidate_count=1", target)
                result = persist_scripture(item, options["dry_run"])
                counts[result] += 1
        except WolClientError as exc:
            logger.warning("event=WOL_PARSE_FAIL source=scripture reason=%s", exc.__class__.__name__)
            raise CommandError(str(exc))
        logger.info("event=CRAWLER_COMMAND_SUMMARY source=scripture inserted=%s skipped=%s", counts["inserted"], counts["skipped"])
        self.stdout.write("inserted=%s skipped=%s dry_run=%s" % (counts["inserted"], counts["skipped"], options["dry_run"]))

