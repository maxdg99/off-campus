# Generated by Django 3.0.4 on 2020-08-01 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0016_auto_20200605_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='campus_area',
            field=models.CharField(choices=[('west', 'West Campus'), ('south', 'South Campus'), ('east', 'East Campus (Univ. District)'), ('north', 'North Campus')], default='east', max_length=6),
            preserve_default=False,
        ),
    ]
