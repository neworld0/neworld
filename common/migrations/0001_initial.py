# Generated by Django 3.1.3 on 2021-09-17 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def forwards_func(apps, schema_editor):
    # 현재 모든 유저에 대해 Profile을 만들어주자.
    # settings.AUTH_USER_MODEL = 'auth.User'
    auth_user_model = settings.AUTH_USER_MODEL.split('.')
    # *는 언팩킹함
    User = apps.get_model(*auth_user_model)
    Profile = apps.get_model('common', 'Profile')

    for user in User.objects.all():
        print('create profile for user#{}'.format(user.pk))
        Profile.objects.create(user=user)

def backwards_func(apps, schema_editor):
    pass



class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('website_url', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(forwards_func, backwards_func),
    ]
