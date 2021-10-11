from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2", "email")


# class GroupForm(UserCreationForm):
#
#     class Meta:
#         model = Group
#         fields = '__all__'

# class UserForm(UserCreationForm):
#
#     class Meta:
#         model = User
#         fields = '__all__'


# from django.contrib.auth.forms import UserCreationForm
# from django.core.validators import validate_email
# from common.models import User
#
#
# class UserForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].validators = [validate_email]
#         self.fields['username'].help_text = '이메일 형식을 입력하세요.'
#         self.fields['username'].label = 'Email'
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = user.username
#         if commit:
#             user.save()
#         return user
#
#     class Meta(UserCreationForm.Meta):
#         model = User


