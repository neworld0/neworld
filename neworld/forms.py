from django import forms
from neworld.models import Question, Answer, Meditation, Comment, Research


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class MeditationForm(forms.ModelForm):
    class Meta:
        model = Meditation
        fields = ['meditation']
        labels = {
            'meditation': '묵상내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }


class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ['content']
        labels = {
            'content': '조사내용',
        }

