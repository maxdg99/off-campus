# Generated by Django 2.2.6 on 2020-09-02 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0013_auto_20200518_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='zipcode',
            field=models.CharField(default='', max_length=5),
        ),
    ]
