# Generated by Django 2.2.6 on 2020-05-13 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0008_auto_20200513_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='beds',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
