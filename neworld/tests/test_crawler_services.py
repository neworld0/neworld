import datetime
from unittest.mock import Mock

import requests
from django.test import SimpleTestCase, TestCase

from neworld.models import Scripture, WeeklyBible
from neworld.services.crawler import persist_scripture, persist_weeklybible
from neworld.services.scripture_parser import ParsedScripture
from neworld.services.weeklybible_parser import ParsedWeeklyBible
from neworld.services.wol_client import (WolClient, WolClientError,
                                          WolHttpStatusError, WolTimeoutError)


class WolClientTests(SimpleTestCase):
    def response(self, status=200, content=b"<html>ok</html>", content_type="text/html", url="https://wol.jw.org/path"):
        response = Mock(status_code=status, content=content, headers={"Content-Type": content_type}, url=url, encoding="utf-8")
        response.text = content.decode("utf-8")
        return response

    def test_valid_html(self):
        session = Mock(); session.get.return_value = self.response()
        self.assertIn("ok", WolClient(session=session).get_html("https://wol.jw.org/path").text)

    def test_bad_responses(self):
        cases = ((202, b"", "text/html"), (403, b"no", "text/html"), (429, b"no", "text/html"),
                 (500, b"no", "text/html"), (200, b"data", "application/json"))
        for status, body, content_type in cases:
            session = Mock(); session.get.return_value = self.response(status, body, content_type)
            with self.subTest(status=status), self.assertRaises(WolClientError):
                WolClient(session=session).get_html("https://wol.jw.org/path")

    def test_timeout_and_connection_error(self):
        for error, expected in ((requests.Timeout(), WolTimeoutError), (requests.ConnectionError(), WolClientError)):
            session = Mock(); session.get.side_effect = error
            with self.assertRaises(expected):
                WolClient(session=session).get_html("https://wol.jw.org/path")

    def test_size_and_redirect_host(self):
        session = Mock(); session.get.return_value = self.response(content=b"1234")
        with self.assertRaises(WolClientError):
            WolClient(session=session, max_bytes=3).get_html("https://wol.jw.org/path")
        session.get.return_value = self.response(url="https://example.com/login")
        with self.assertRaises(WolClientError):
            WolClient(session=session).get_html("https://wol.jw.org/path")


class PersistenceTests(TestCase):
    def test_placeholder_is_not_saved(self):
        item = ParsedScripture(datetime.date(2026, 8, 23), "데이터 준비 중", "body", "url")
        self.assertEqual(persist_scripture(item), "skipped")
        self.assertFalse(Scripture.objects.exists())

    def test_existing_date_is_not_overwritten_and_is_idempotent(self):
        item = ParsedScripture(datetime.date(2026, 8, 23), "성구", "해설", "url")
        Scripture.objects.create(scripture="old", bodytext="old", real_date="2026-08-23")
        self.assertEqual(persist_scripture(item), "skipped")
        self.assertEqual(persist_scripture(item), "skipped")
        self.assertEqual(Scripture.objects.count(), 1)

    def test_weekly_deduplicates_specific_id_and_week(self):
        item = ParsedWeeklyBible(2026, 35, "주간", "범위", "https://wol.jw.org/x", "202026321")
        self.assertEqual(persist_weeklybible(item), "inserted")
        self.assertEqual(persist_weeklybible(item), "skipped")
        self.assertEqual(WeeklyBible.objects.count(), 1)
