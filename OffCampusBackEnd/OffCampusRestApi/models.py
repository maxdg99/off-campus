from django.db import models

class Listing(models.Model):
    AVAILABILITY_MODE = ['Season', 'Month', 'Now', 'None', 'Date']

    price = models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=100)
    unit = models.CharField(null=True, max_length=10)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.FloatField()
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, null=True)
    miles_from_campus = models.FloatField(null=True)
    url = models.CharField(max_length=1000)
    availability_date = models.DateField(null=True)
    availability_mode = models.CharField(max_length=10, choices=AVAILABILITY_MODE)
    listed = models.BooleanField()
    date_found = models.DateField()
    date_updated = models.DateField()

    percent_diff = None # populated at runtime
    diff_raw = 0

    listings = models.Manager()

class User(models.Model):
    google_id = models.CharField(max_length=64, null=True)
    favorites = models.ManyToManyField(Listing)