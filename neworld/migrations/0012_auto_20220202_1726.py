# Generated by Django 3.1.3 on 2022-02-02 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neworld', '0011_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='positon',
            new_name='position',
        ),
    ]
