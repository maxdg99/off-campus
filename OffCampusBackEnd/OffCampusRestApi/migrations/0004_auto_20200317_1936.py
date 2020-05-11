# Generated by Django 2.2.6 on 2020-03-17 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0003_auto_20191219_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='listing',
            name='scraper',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='listing',
            name='unit',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='google_id',
            field=models.CharField(default='', max_length=64),
        ),
    ]