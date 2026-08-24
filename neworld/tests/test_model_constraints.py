from django.db import IntegrityError, transaction
from django.test import TestCase

from neworld.models import Answer, Bible, Comment, Question, Scripture, WeeklyBible


class ModelConstraintTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(subject="질문", content="내용")
        self.answer = Answer.objects.create(question=self.question, content="답변")

    def test_comment_requires_exactly_one_target(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Comment.objects.create(content="대상 없음")

        with self.assertRaises(IntegrityError), transaction.atomic():
            Comment.objects.create(
                content="대상 둘", question=self.question, answer=self.answer)

        comment = Comment.objects.create(content="유효", question=self.question)
        self.assertEqual(comment.question_id, self.question.id)

    def test_weekly_bible_year_and_week_are_unique(self):
        WeeklyBible.objects.create(year=2026, n_week=35, week="주간", bible_range="범위")
        with self.assertRaises(IntegrityError), transaction.atomic():
            WeeklyBible.objects.create(year=2026, n_week=35, week="다른 주간", bible_range="다른 범위")

    def test_scripture_real_date_is_unique(self):
        Scripture.objects.create(scripture="성구", bodytext="본문", real_date="2026-08-24")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Scripture.objects.create(scripture="다른 성구", bodytext="다른 본문", real_date="2026-08-24")

    def test_bible_id_is_unique(self):
        Bible.objects.create(bible_id="GEN", bible="창세기")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Bible.objects.create(bible_id="GEN", bible="중복 창세기")
