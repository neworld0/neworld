from django import forms
from neworld.models import Question, Answer, Meditation, Comment, Research, Customer, Activity


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
            'content': '묵상 및 조사내용',
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['area', 'name', 'keyman', 'position', 'grade', 'tel', 'address', 'email', 'remark']
        labels = {
            'area': '지역',
            'name': '단체명',
            'keyman': 'Keyman',
            'position': '직위',
            'grade': '추진등급(A/B/C)',
            'tel': '전화번호',
            'address': '주소',
            'email': '이메일',
            'remark': '특이사항',
        }


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['content']
        labels = {
            'content': '활동내용',
        }
