# Generated by Django 3.1.3 on 2021-08-31 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neworld', '0006_auto_20210831_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bibleweek',
            name='bible_range',
        ),
        migrations.RemoveField(
            model_name='bibleweek',
            name='week',
        ),
    ]