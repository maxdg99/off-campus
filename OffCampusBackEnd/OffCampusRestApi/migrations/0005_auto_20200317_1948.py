# Generated by Django 2.2.6 on 2020-03-17 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0005_auto_20191221_1959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='date_found',
            new_name='date_created',
        ),
    ]
