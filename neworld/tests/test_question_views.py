from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from neworld.models import Answer, Question


class QuestionListViewTests(TestCase):
    def setUp(self):
        self.viewer = User.objects.create_user(username='question-viewer', password='test-password')
        self.author = User.objects.create_user(username='question-author', password='test-password')
        self.recommended = Question.objects.create(
            author=self.author, subject='추천 많은 글', content='내용')
        self.popular = Question.objects.create(
            author=self.author, subject='답변 많은 글', content='내용')
        self.recommended.voter.add(self.viewer)
        Answer.objects.create(question=self.popular, author=self.author, content='답변 1')
        Answer.objects.create(question=self.popular, author=self.viewer, content='답변 2')
        self.client.force_login(self.viewer)

    def test_recommend_order_and_count(self):
        response = self.client.get(reverse('neworld:question'), {'so': 'recommend'})

        questions = list(response.context['question_list'].object_list)
        self.assertEqual(questions[0], self.recommended)
        self.assertEqual(questions[0].num_voter, 1)
        self.assertContains(response, 'badge bg-warning text-dark px-2 py-1')

    def test_popular_order_uses_answer_count(self):
        response = self.client.get(reverse('neworld:question'), {'so': 'popular'})

        questions = list(response.context['question_list'].object_list)
        self.assertEqual(questions[0], self.popular)
        self.assertEqual(questions[0].num_answer, 2)
