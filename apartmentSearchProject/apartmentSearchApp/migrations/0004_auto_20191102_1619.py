# Generated by Django 2.2.6 on 2019-11-02 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartmentSearchApp', '0003_auto_20191102_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
