# Generated by Django 3.0.4 on 2021-01-23 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffCampusRestApi', '0017_listing_campus_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='availability_mode',
            field=models.CharField(choices=[('S', 'Season'), ('M', 'Month'), ('N', 'Now'), ('-', 'None'), ('D', 'Date')], default='-', max_length=2),
        ),
        migrations.AlterField(
            model_name='listing',
            name='campus_area',
            field=models.CharField(choices=[('north', 'North Campus'), ('northeast', 'Northeast Campus'), ('northwest', 'Northwest Campus'), ('south', 'South Campus'), ('southeast', 'Southeast Campus'), ('southwest', 'Southwest Campus')], max_length=10),
        ),
        migrations.AlterField(
            model_name='listing',
            name='street_range',
            field=models.CharField(default='', max_length=25),
        ),
    ]
