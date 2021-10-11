from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.core.mail import send_mail
# from django.contrib.auth.models import AbstractUser



# class User(AbstractUser):
#     username = models.CharField(db_index=True, unique=True, max_length=255)
#     first_name = models.CharField(max_length=150, null=True)
#     last_name = models.CharField(max_length=150, null=True)
#     nickname = models.CharField(max_length=150, null=True)
#     password = models.CharField(max_length=128, null=False)
#     is_superuser = models.BooleanField(null=True)
#     is_staff = models.BooleanField(null=True)
#     is_active = models.BooleanField(null=True)
#     email = models.EmailField(unique=True, blank=True)
#     last_login = models.DateTimeField(auto_created=True, null=True)
#     date_joined = models.DateTimeField(auto_created=True, null=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)


def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)

# User 회원 가입 시 Profile 생성하기
post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)


# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'neworld0@gmial.com',
#     ['neworld@me.com'],
#     fail_silently=False,
# )
