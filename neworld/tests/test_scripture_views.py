import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from neworld.models import Meditation, Scripture


class ScriptureListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='scripture-user', password='test-password')
        self.recommended = Scripture.objects.create(
            scripture='추천 성구', bodytext='추천 본문', real_date='2026-01-01')
        self.other = Scripture.objects.create(
            scripture='일반 성구', bodytext='일반 본문', real_date='2026-01-02')
        meditation = Meditation.objects.create(
            scripture=self.recommended, author=self.user, meditation='묵상', real_date='2026-01-01')
        meditation.voter.add(self.user)
        self.client.force_login(self.user)

    def test_recommend_order_uses_meditation_votes(self):
        response = self.client.get(reverse('neworld:scripture'), {'so': 'recommend'})

        self.assertEqual(response.status_code, 200)
        scriptures = list(response.context['scripture_list'].object_list)
        self.assertEqual(scriptures[0], self.recommended)
        self.assertEqual(scriptures[0].num_voter, 1)

    def test_default_list_includes_meditation_vote_count(self):
        response = self.client.get(reverse('neworld:scripture'))

        recommended = next(
            scripture for scripture in response.context['scripture_list'].object_list
            if scripture.id == self.recommended.id)
        self.assertEqual(recommended.num_voter, 1)
        self.assertContains(response, 'badge bg-warning text-dark px-2 py-1')

    def test_keyword_search_does_not_query_missing_scripture_author(self):
        response = self.client.get(reverse('neworld:scripture'), {'kw': '추천'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '추천 성구')

    def test_list_orders_tomorrow_before_today(self):
        today = datetime.date.today()
        today_scripture = Scripture.objects.create(
            scripture='오늘 성구', bodytext='오늘 본문', real_date=today.isoformat())
        tomorrow_scripture = Scripture.objects.create(
            scripture='내일 성구', bodytext='내일 본문',
            real_date=(today + datetime.timedelta(days=1)).isoformat())

        response = self.client.get(reverse('neworld:scripture'))
        scriptures = list(response.context['scripture_list'].object_list)

        self.assertEqual(scriptures[:2], [tomorrow_scripture, today_scripture])
        self.assertEqual(response.context['today_scripture'], today_scripture)

    def test_today_scripture_is_shown_outside_the_current_list_page(self):
        today = datetime.date.today()
        Scripture.objects.create(
            scripture='항상 보이는 오늘 성구', bodytext='오늘 본문', real_date=today.isoformat())
        for day in range(11):
            Scripture.objects.create(
                scripture='다른 성구 %s' % day,
                bodytext='본문',
                real_date=(today - datetime.timedelta(days=day + 10)).isoformat())

        response = self.client.get(reverse('neworld:scripture'), {'page': 2})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '항상 보이는 오늘 성구')
        self.assertEqual(response.context['scripture_list'].number, 2)
