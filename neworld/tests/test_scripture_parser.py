import datetime

from django.test import SimpleTestCase

from neworld.services.scripture_parser import parse_annual_scripture, parse_annual_scripture_link, parse_monthly_scriptures, parse_scripture
from neworld.services.wol_client import WolClientError
from neworld.tests.helpers import fixture


class ScriptureParserTests(SimpleTestCase):
    target = datetime.date(2026, 8, 23)

    def test_normal_unicode_and_date(self):
        item = parse_scripture(fixture("daily_normal.html"), self.target, "https://wol.jw.org/example")
        self.assertEqual(item.source_date, self.target)
        self.assertIn("한국어", item.body_text)

    def test_reordered_semantic_markup(self):
        item = parse_scripture(fixture("daily_reordered.html"), self.target, "https://wol.jw.org/example")
        self.assertEqual(item.scripture_text, "순서가 바뀐 성구")

    def test_multiple_selects_target_date(self):
        item = parse_scripture(fixture("daily_multiple.html"), self.target, "https://wol.jw.org/example")
        self.assertEqual(item.scripture_text, "오늘")

    def test_invalid_documents_are_controlled(self):
        for name in ("daily_missing_scripture.html", "daily_missing_body.html", "daily_empty.html", "interstitial.html"):
            with self.subTest(name=name), self.assertRaises(WolClientError):
                parse_scripture(fixture(name), self.target, "https://wol.jw.org/example")

    def test_date_mismatch_is_rejected(self):
        with self.assertRaises(WolClientError):
            parse_scripture(fixture("daily_normal.html"), datetime.date(2026, 8, 24), "https://wol.jw.org/example")

    def test_annual_document_extracts_a_future_date(self):
        list_html = '<a href="/ko/wol/d/r8/lp-ko/1102026207">\ub0a0\ub9c8\ub2e4 \uc131\uacbd\uc744 \uac80\ud1a0\ud568?2026</a>'
        source_url = parse_annual_scripture_link(list_html, 2026, "https://wol.jw.org/list")
        annual_html = '''
            <p>8\uc6d4 24\uc77c</p><p class="themeScrp">Tomorrow verse</p>
            <p class="sb">First explanation</p><p class="sb">Second explanation</p>
            <p>8\uc6d4 25\uc77c</p><p class="themeScrp">Next verse</p><p class="sb">Next explanation</p>
        '''

        item = parse_annual_scripture(annual_html, datetime.date(2026, 8, 24), source_url)

        self.assertEqual(source_url, "https://wol.jw.org/ko/wol/d/r8/lp-ko/1102026207")
        self.assertEqual(item.scripture_text, "Tomorrow verse")
        self.assertIn("Second explanation", item.body_text)
    def test_monthly_document_requires_all_dates(self):
        monthly_html = "".join(
            '<p>8\uc6d4 %s\uc77c</p><p class="themeScrp">Verse %s</p><p class="sb">Body %s</p>' % (day, day, day)
            for day in range(1, 32)
        )

        items = parse_monthly_scriptures(monthly_html, 2026, 8, "file:///saved.html")

        self.assertEqual(len(items), 31)
        self.assertEqual(items[-1].source_date, datetime.date(2026, 8, 31))
