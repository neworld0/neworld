# Generated by Django 3.1.3 on 2021-08-31 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neworld', '0005_bibleweek'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibleweek',
            name='n_week',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='bibleweek',
            name='week',
            field=models.CharField(max_length=50),
        ),
    ]
