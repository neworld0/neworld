# Generated by Django 3.1.3 on 2021-09-16 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neworld', '0024_auto_20210911_2030'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'permissions': [('can_publish', 'Can Publish Posts')]},
        ),
        migrations.AlterModelOptions(
            name='meditation',
            options={'permissions': [('can_publish', 'Can Publish Posts')]},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'permissions': [('can_publish', 'Can Publish Posts')]},
        ),
        migrations.AlterModelOptions(
            name='research',
            options={'permissions': [('can_publish', 'Can Publish Posts')]},
        ),
        migrations.AlterModelOptions(
            name='weeklybible',
            options={'permissions': [('can_publish', 'Can Publish Posts')]},
        ),
    ]
