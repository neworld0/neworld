# Generated by Django 3.1.3 on 2022-12-28 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('neworld', '0019_auto_20220304_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gpt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_gpt', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('voter', models.ManyToManyField(null=True, related_name='voter_gpt', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_publish', 'Can Publish Posts'), ('can_change', 'Can Change Posts'), ('can_view', 'Can View Posts'), ('can_delete', 'Can Delete Posts')],
            },
        ),
        migrations.CreateModel(
            name='GptAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_gptanswer', to=settings.AUTH_USER_MODEL)),
                ('gpt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neworld.gpt')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('voter', models.ManyToManyField(null=True, related_name='voter_gptanswer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_publish', 'Can Publish Posts'), ('can_change', 'Can Change Posts'), ('can_view', 'Can View Posts'), ('can_delete', 'Can Delete Posts')],
            },
        ),
    ]
