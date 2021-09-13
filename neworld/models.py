from django.db import models
from django.contrib.auth.models import User, Group

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question', null=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question', null=True)
    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer', null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer', null=True)
    def __str__(self):
        return self.content

class Scripture(models.Model):
    scripture = models.CharField(max_length=400)
    bodytext = models.TextField()
    real_date = models.CharField(max_length=10)
    d_week = models.CharField(max_length=50, null=True)
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_scripture', null=True)
    def __str__(self):
        return self.real_date

class Meditation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_meditation', null=True)
    scripture = models.ForeignKey(Scripture, on_delete=models.CASCADE)
    meditation = models.TextField()
    real_date = models.CharField(max_length=10)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_meditation', null=True)
    def __str__(self):
        return self.real_date

class Bible(models.Model):
    bible_id = models.CharField(max_length=10)
    bible = models.CharField(max_length=30)
    def __str__(self):
        return self.bible

class WeeklyBible(models.Model):
    year = models.CharField(max_length=10)
    n_week = models.CharField(max_length=10)
    week = models.CharField(max_length=100)
    bible_range = models.CharField(max_length=100)
    bible_link = models.URLField('Site URL', null=True, blank=True)
    specific_id = models.CharField(max_length=50, null=True, blank=True)
    create_date = models.DateTimeField()
    def __str__(self):
        return self.week

class WBsummary(models.Model):
    weeklybible = models.ForeignKey(WeeklyBible, on_delete=models.CASCADE, null=True)
    bible = models.ForeignKey(Bible, on_delete=models.CASCADE, null=True)
    chapter = models.CharField(max_length=10)
    bible_summary = models.TextField()
    specific_id = models.CharField(max_length=50, null=True, blank=True)
    create_date = models.DateTimeField()
    def __str__(self):
        return self.bible_summary

class Research(models.Model):
    weeklybible = models.ForeignKey(WeeklyBible, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_research', null=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_research', null=True)
    def __str__(self):
        return self.content

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    meditation = models.ForeignKey(Meditation, null=True, blank=True, on_delete=models.CASCADE)
    research = models.ForeignKey(Research, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.content

