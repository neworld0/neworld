import datetime

from django.test import SimpleTestCase

from neworld.services.weeklybible_parser import next_iso_week, parse_weeklybible
from neworld.services.wol_client import WolClientError
from neworld.tests.helpers import fixture


class WeeklyBibleParserTests(SimpleTestCase):
    def test_normal_and_reordered(self):
        first = parse_weeklybible(fixture("weekly_normal.html"), 2026, 35, "https://wol.jw.org/example")
        second = parse_weeklybible(fixture("weekly_reordered.html"), 2026, 36, "https://wol.jw.org/example")
        self.assertEqual(first.specific_id, "202026321")
        self.assertNotIn("?", second.bible_link)

    def test_invalid_documents_are_controlled(self):
        for name in ("weekly_missing_header.html", "weekly_missing_link.html", "weekly_empty.html", "interstitial.html"):
            with self.subTest(name=name), self.assertRaises(WolClientError):
                parse_weeklybible(fixture(name), 2026, 35, "https://wol.jw.org/example")

    def test_iso_year_boundaries(self):
        self.assertEqual(next_iso_week(datetime.date(2020, 12, 28)), (2021, 1))
        self.assertEqual(next_iso_week(datetime.date(2021, 12, 27)), (2022, 1))
        self.assertEqual(next_iso_week(datetime.date(2019, 12, 30)), (2020, 2))
