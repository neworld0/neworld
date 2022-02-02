from django.db import models
from django.contrib.auth.models import User, Group
from django.shortcuts import reverse


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question', null=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question', null=True)
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
    voter = models.ManyToManyField(User, related_name='voter_answer', null=True)
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
    year = models.CharField(max_length=10)
    n_week = models.CharField(max_length=10)
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
    def __str__(self):
        return self.week

    def get_absolute_url(self):
        return reverse("neworld:weeklybible", kwargs={"pk": self.pk})


class Scripture(models.Model):
    scripture = models.CharField(max_length=400)
    bodytext = models.TextField()
    real_date = models.CharField(max_length=10)
    d_week = models.CharField(max_length=50, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.real_date


class Meditation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_meditation', null=True)
    scripture = models.ForeignKey(Scripture, on_delete=models.CASCADE)
    meditation = models.TextField()
    real_date = models.CharField(max_length=10)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_meditation', null=True)
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
    voter = models.ManyToManyField(User, related_name='voter_research', null=True)
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
    name = models.TextField()
    keyman = models.TextField()
    position = models.TextField()
    grade = models.CharField(max_length=2)
    remark = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_customer', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_activity', null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_activity', null=True)
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