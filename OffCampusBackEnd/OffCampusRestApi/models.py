from django.db import models

class Listing(models.Model):
    AREA_CHOICES = [('N', 'North Campus'), ('S', 'South Campus')]

    price = models.PositiveIntegerField(null=True)
    address = models.CharField(max_length=100)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.FloatField()
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    miles_from_campus = models.FloatField(null=True)
    area_of_campus = models.CharField(max_length=10, choices=AREA_CHOICES)
    url = models.CharField(max_length=1000)
    availability_date = models.DateField(null=True)
    active = models.BooleanField()

    percent_diff = None # populated at runtime
    diff_raw = 0

    listings = models.Manager()