from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.shortcuts import reverse


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question', null=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = [
            ('can_publish', 'Can Publish Posts'),
            ('can_change', 'Can Change Posts'),
            ('can_view', 'Can View Posts'),
            ('can_delete', 'Can Delete Posts'),
        ]

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("neworld:question_list", kwargs={"pk": self.pk})


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer', null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = [
            ('can_publish', 'Can Publish Posts'),
            ('can_change', 'Can Change Posts'),
            ('can_view', 'Can View Posts'),
            ('can_delete', 'Can Delete Posts'),
        ]

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("neworld:question_detail", kwargs={"pk": self.pk})


class WeeklyBible(models.Model):
    year = models.IntegerField()
    n_week = models.IntegerField()
    week = models.CharField(max_length=100)
    bible_range = models.CharField(max_length=100)
    bible_link = models.URLField('Site URL', null=True, blank=True)
    specific_id = models.CharField(max_length=50, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ('can_publish', 'Can Publish Posts'),
            ('can_change', 'Can Change Posts'),
            ('can_view', 'Can View Posts'),
            ('can_delete', 'Can Delete Posts'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['year', 'n_week'], name='weeklybible_year_week_uniq'),
        ]

    def __str__(self):
        return self.week

    def get_absolute_url(self):
        # noinspection SpellCheckingInspection
        return reverse("neworld:weeklybible", kwargs={"pk": self.pk})


class Scripture(models.Model):
    scripture = models.CharField(max_length=400)
    bodytext = models.TextField()
    real_date = models.CharField(max_length=10)
    d_week = models.CharField(max_length=50, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.real_date

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['real_date'], name='scripture_real_date_uniq'),
        ]


class Meditation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_meditation', null=True)
    scripture = models.ForeignKey(Scripture, on_delete=models.CASCADE)
    meditation = models.TextField()
    real_date = models.CharField(max_length=10)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_meditation')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = [
            ('can_publish', 'Can Publish Posts'),
            ('can_change', 'Can Change Posts'),
            ('can_view', 'Can View Posts'),
            ('can_delete', 'Can Delete Posts'),
        ]

    def __str__(self):
        return self.real_date

    def get_absolute_url(self):
        return reverse("neworld:daily_scripture", kwargs={"pk": self.pk})


class Bible(models.Model):
    bible_id = models.CharField(max_length=10)
    bible = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.bible

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['bible_id'], name='bible_bible_id_uniq'),
        ]


class WBsummary(models.Model):
    weeklybible = models.ForeignKey(WeeklyBible, on_delete=models.CASCADE, null=True)
    bible = models.ForeignKey(Bible, on_delete=models.CASCADE, null=True)
    chapter = models.CharField(max_length=10)
    bible_summary = models.TextField()
    specific_id = models.CharField(max_length=50, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chapter


class PubsIndex(models.Model):
    weeklybible = models.ForeignKey(WeeklyBible, on_delete=models.CASCADE, null=True)
    bible = models.ForeignKey(Bible, on_delete=models.CASCADE, null=True)
    chapter = models.CharField(max_length=10)
    index_verse = models.CharField(max_length=50)
    pi_title = models.CharField(max_length=50)
    pi_link = models.URLField('Publications Index URL', null=True, blank=True)
    specific_id = models.CharField(max_length=50, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pi_title


class Research(models.Model):
    weeklybible = models.ForeignKey(WeeklyBible, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_research', null=True)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_research')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = [
            ('can_publish', 'Can Publish Posts'),
            ('can_change', 'Can Change Posts'),
            ('can_view', 'Can View Posts'),
            ('can_delete', 'Can Delete Posts'),
        ]

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("neworld:weeklybible_detail", kwargs={"pk": self.pk})


class Customer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_customer', null=True)
    area = models.TextField(null=True, blank=True)
    name = models.TextField()
    keyman = models.TextField()
    position = models.TextField()
    grade = models.CharField(max_length=2)
    tel = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_customer')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_activity', null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_activity')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    meditation = models.ForeignKey(Meditation, null=True, blank=True, on_delete=models.CASCADE)
    research = models.ForeignKey(Research, null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, null=True, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(question__isnull=False, answer__isnull=True, meditation__isnull=True,
                      research__isnull=True, customer__isnull=True, activity__isnull=True)
                    | Q(question__isnull=True, answer__isnull=False, meditation__isnull=True,
                        research__isnull=True, customer__isnull=True, activity__isnull=True)
                    | Q(question__isnull=True, answer__isnull=True, meditation__isnull=False,
                        research__isnull=True, customer__isnull=True, activity__isnull=True)
                    | Q(question__isnull=True, answer__isnull=True, meditation__isnull=True,
                        research__isnull=False, customer__isnull=True, activity__isnull=True)
                    | Q(question__isnull=True, answer__isnull=True, meditation__isnull=True,
                        research__isnull=True, customer__isnull=False, activity__isnull=True)
                    | Q(question__isnull=True, answer__isnull=True, meditation__isnull=True,
                        research__isnull=True, customer__isnull=True, activity__isnull=False)
                ),
                name='comment_exactly_one_target',
            ),
        ]


class Gpt(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_gpt', null=True)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_gpt')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = [
            ('can_publish', 'Can Publish Posts'),
            ('can_change', 'Can Change Posts'),
            ('can_view', 'Can View Posts'),
            ('can_delete', 'Can Delete Posts'),
        ]

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("neworld:gpt_list", kwargs={"pk": self.pk})


class GptAnswer(models.Model):
    gpt = models.ForeignKey(Gpt, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    voter = models.ManyToManyField(User, related_name='voter_gptanswer')

    class Meta:
        permissions = [
            ('can_publish', 'Can Publish Posts'),
            ('can_change', 'Can Change Posts'),
            ('can_view', 'Can View Posts'),
            ('can_delete', 'Can Delete Posts'),
        ]

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("neworld:gpt_detail", kwargs={"pk": self.pk})
