# Generated by Django 2.2.6 on 2020-06-06 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0010_auto_20200514_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='pretty_address',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
