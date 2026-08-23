import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from neworld.models import Scripture, WeeklyBible


class CrawlerViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="offline-user", password="test-password")

    @patch("neworld.views.base_views.prefetch_future_scriptures")
    def test_home_prefetches_after_current_duplicate_safely(self, prefetch):
        today = datetime.date.today().isoformat()
        Scripture.objects.create(scripture="first", bodytext="body", real_date=today, d_week="일")
        Scripture.objects.create(scripture="second", bodytext="body", real_date=today, d_week="일")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["scripture_html"], "first")
        prefetch.assert_called_once_with(datetime.date.today())

    def test_home_historical_and_empty_fallbacks(self):
        response = self.client.get(reverse("index"))
        self.assertTrue(response.context["scripture_is_empty"])
        Scripture.objects.create(scripture="saved", bodytext="saved body", real_date="2020-01-01")
        response = self.client.get(reverse("index"))
        self.assertTrue(response.context["scripture_is_fallback"])

    @patch("requests.get", side_effect=AssertionError("view attempted network"))
    def test_weekly_failure_cannot_hide_saved_rows(self, unused):
        self.client.force_login(self.user)
        WeeklyBible.objects.create(year=2020, n_week=1, week="saved week", bible_range="saved range")
        response = self.client.get(reverse("neworld:weeklybible"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "saved range")
        self.assertTrue(response.context["weeklybible_is_fallback"])

    def test_weekly_empty_state(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("neworld:weeklybible"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["weeklybible_is_empty"])

