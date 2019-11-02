# Generated by Django 2.2.6 on 2019-11-02 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_1', models.CharField(max_length=100)),
                ('line_2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('zip_code', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_bedrooms', models.PositiveIntegerField()),
                ('num_bathrooms', models.FloatField()),
                ('image_url', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('miles_from_campus', models.FloatField()),
                ('area_of_campus', models.CharField(choices=[('N', 'North Campus'), ('S', 'South Campus')], max_length=10)),
                ('url', models.CharField(max_length=1000)),
                ('availability_date', models.DateField()),
                ('active', models.BooleanField()),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='apartmentSearchApp.Address')),
            ],
        ),
    ]
