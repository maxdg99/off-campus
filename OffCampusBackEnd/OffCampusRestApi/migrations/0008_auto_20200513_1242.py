# Generated by Django 2.2.6 on 2020-05-13 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0007_auto_20200510_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='baths',
            field=models.FloatField(null=True),
        ),
    ]
