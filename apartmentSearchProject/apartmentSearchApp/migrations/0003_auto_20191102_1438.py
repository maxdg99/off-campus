# Generated by Django 2.2.6 on 2019-11-02 18:38

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('apartmentSearchApp', '0002_auto_20191102_1350'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='listing',
            managers=[
                ('listings', django.db.models.manager.Manager()),
            ],
        ),
    ]