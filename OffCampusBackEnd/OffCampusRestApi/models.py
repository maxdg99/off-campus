from django.db import models

class Listing(models.Model):
    AVAILABILITY_MODE = [('S', 'Season'), ('M', 'Month'), ('N', 'Now'), ('-', 'None'), ('D', 'Date')]

    price = models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=100)
    date_created = models.DateField()
    date_updated = models.DateField()
    unit = models.CharField(max_length=10, default="")
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.FloatField()
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, default="")
    miles_from_campus = models.FloatField(null=True)
    url = models.CharField(max_length=1000)
    availability_date = models.DateField(null=True)
    availability_mode = models.CharField(max_length=2, choices=AVAILABILITY_MODE)
    active = models.BooleanField()
    scraper = models.CharField(max_length=100, default="")

    percent_diff = None # populated at runtime
    diff_raw = 0

    listings = models.Manager()

class User(models.Model):
    google_id = models.CharField(max_length=64, default="")
    favorites = models.ManyToManyField(Listing)