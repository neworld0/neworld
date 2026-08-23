from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from neworld.services.crawler import persist_scripture
from neworld.services.scripture_parser import parse_monthly_scriptures
from neworld.services.wol_client import WolClientError


def read_saved_html(path):
    """Read a browser-saved document without making a network request."""
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise CommandError("Cannot read HTML file: %s" % exc) from exc
    if not raw.strip():
        raise CommandError("HTML file is empty")
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise CommandError("HTML file must be UTF-8 or CP949 encoded")


class Command(BaseCommand):
    help = "Import one full month of Scripture from a browser-saved WOL HTML file."

    def add_arguments(self, parser):
        parser.add_argument("html_file", help="Path to the browser-saved monthly WOL HTML file")
        parser.add_argument("--year", required=True, type=int)
        parser.add_argument("--month", required=True, type=int)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        year, month = options["year"], options["month"]
        if not 1 <= month <= 12:
            raise CommandError("--month must be between 1 and 12")
        html_path = Path(options["html_file"])
        html = read_saved_html(html_path)
        try:
            items = parse_monthly_scriptures(html, year, month, html_path.resolve().as_uri())
        except WolClientError as exc:
            raise CommandError("Saved HTML is not a valid monthly Scripture document: %s" % exc) from exc

        counts = {"inserted": 0, "skipped": 0}
        for item in items:
            counts[persist_scripture(item, options["dry_run"])] += 1
        self.stdout.write(
            "month=%04d-%02d parsed=%s inserted=%s skipped=%s dry_run=%s" % (
                year, month, len(items), counts["inserted"], counts["skipped"], options["dry_run"])
        )
