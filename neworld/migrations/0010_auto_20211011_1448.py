# Generated by Django 3.1.3 on 2021-10-11 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('neworld', '0009_auto_20211011_0043'),
    ]

    operations = [
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
