from django.db import models

class Listing(models.Model):
    AVAILABILITY_MODE = [('S', 'Season'), ('M', 'Month'), ('N', 'Now'), ('-', 'None'), ('D', 'Date')]

    url = models.CharField(max_length=1000)
    
    image = models.CharField(max_length=1000)
    
    address = models.CharField(max_length=100)
    unit = models.CharField(max_length=10, default="")

    beds = models.PositiveIntegerField(null=True)
    baths = models.FloatField(null=True)

    description = models.CharField(max_length=1000, default="")

    price = models.PositiveIntegerField(null=True)

    availability_date = models.DateField(null=True)
    availability_mode = models.CharField(max_length=2, choices=AVAILABILITY_MODE)

    active = models.BooleanField()

    date_created = models.DateField()
    date_updated = models.DateField()

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    
    miles_from_campus = models.FloatField(null=True)
    
    scraper = models.CharField(max_length=100, default="")

    percent_diff = None # populated at runtime
    diff_raw = 0

    listings = models.Manager()

class User(models.Model):
    google_id = models.CharField(max_length=64, default="")
    favorites = models.ManyToManyField(Listing)