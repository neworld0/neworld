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

    def test_keyword_search_does_not_query_missing_scripture_author(self):
        response = self.client.get(reverse('neworld:scripture'), {'kw': '추천'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '추천 성구')
