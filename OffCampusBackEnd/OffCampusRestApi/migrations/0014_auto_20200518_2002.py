# Generated by Django 2.2.6 on 2020-05-19 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0013_auto_20200518_2001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='date_found',
            new_name='date_created',
        ),
    ]