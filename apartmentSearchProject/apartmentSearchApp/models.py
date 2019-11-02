from django.db import models

# Create your models here.

class Address(models.Model):
    line_1 = models.CharField(max_length=100)
    line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.PositiveIntegerField()

class Listing(models.Model):
    AREA_CHOICES = [("N", "North Campus"), ("S", "South Campus")]

    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.FloatField()
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    miles_from_campus = models.FloatField()
    area_of_campus = models.CharField(max_length=10, choices=AREA_CHOICES)
    url = models.CharField(max_length=1000)
    availability_date = models.DateField()
    active = models.BooleanField()
    
