# Generated by Django 3.1.3 on 2021-10-10 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('neworld', '0007_auto_20211009_2038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='meditation',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='question',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='research',
            name='groups',
        ),
        migrations.AddField(
            model_name='answer',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
        migrations.AddField(
            model_name='comment',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
        migrations.AddField(
            model_name='meditation',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
        migrations.AddField(
            model_name='question',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
        migrations.AddField(
            model_name='research',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
    ]
