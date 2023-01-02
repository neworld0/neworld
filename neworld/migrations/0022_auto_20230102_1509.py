# Generated by Django 3.1.3 on 2023-01-02 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('neworld', '0021_auto_20230102_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='gptanswer',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_gptanswer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gptanswer',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
        migrations.AddField(
            model_name='gptanswer',
            name='voter',
            field=models.ManyToManyField(null=True, related_name='voter_gptanswer', to=settings.AUTH_USER_MODEL),
        ),
    ]
