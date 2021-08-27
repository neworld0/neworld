from django.db import models
from django.contrib.auth.models import User

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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_scripture', null=True)
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

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    meditation = models.ForeignKey(Meditation, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.content