# Generated by Django 3.1.3 on 2021-09-11 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neworld', '0021_research_n_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bible',
            name='chapter',
        ),
        migrations.RemoveField(
            model_name='bible',
            name='verse',
        ),
        migrations.AlterField(
            model_name='wbsummary',
            name='bible',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neworld.bible'),
        ),
        migrations.AlterField(
            model_name='weeklybible',
            name='bible_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='neworld.bible'),
        ),
    ]
