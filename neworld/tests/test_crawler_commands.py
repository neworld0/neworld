import datetime
import io
import zipfile
from io import StringIO
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from neworld.models import Scripture, WeeklyBible
from neworld.tests.helpers import fixture
from neworld.management.commands.fetch_scriptures import default_collection_window
from neworld.admin import _read_uploaded_txt_zip


class CrawlerCommandTests(TestCase):
    @patch("neworld.management.commands.fetch_scriptures.WolClient")
    def test_scripture_dry_run_has_no_write(self, client_class):
        client_class.return_value.get_html.return_value = Mock(
            text=fixture("daily_normal.html"), url="https://wol.jw.org/example")
        output = StringIO()
        call_command("fetch_scriptures", target_date=datetime.date(2026, 8, 23), dry_run=True, stdout=output)
        self.assertFalse(Scripture.objects.exists())
        self.assertIn("dry_run=True", output.getvalue())
    def test_default_window_prefetches_a_week_after_today_is_saved(self):
        today = datetime.date(2026, 8, 23)
        Scripture.objects.create(
            scripture="today", bodytext="saved", real_date=today.isoformat(), d_week="?")

        start, days = default_collection_window(today)

        self.assertEqual(start, datetime.date(2026, 8, 24))
        self.assertEqual(days, 7)

    def test_default_window_uses_today_without_a_valid_today_row(self):
        today = datetime.date(2026, 8, 23)
        Scripture.objects.create(
            scripture="??? ?? ?", bodytext="saved", real_date=today.isoformat(), d_week="?")

        start, days = default_collection_window(today)


    @patch("neworld.management.commands.fetch_weeklybible.WolClient")
    def test_weekly_command_is_idempotent(self, client_class):
        client_class.return_value.get_html.return_value = Mock(
            text=fixture("weekly_normal.html"), url="https://wol.jw.org/example")
        call_command("fetch_weeklybible", year=2026, week=35, stdout=StringIO())
        call_command("fetch_weeklybible", year=2026, week=35, stdout=StringIO())
        self.assertEqual(WeeklyBible.objects.count(), 1)

    def test_txt_zip_ignores_the_permanent_00_file(self):
        archive_bytes = io.BytesIO()
        with zipfile.ZipFile(archive_bytes, "w") as archive:
            archive.writestr("es26_KO_00.txt", "metadata")
            archive.writestr("es26_KO_01.txt", "January text")
        uploaded = SimpleUploadedFile("es26_KO.txt.zip", archive_bytes.getvalue(), content_type="application/zip")

        monthly_texts = _read_uploaded_txt_zip(uploaded)

        self.assertEqual(monthly_texts, {1: "January text"})
