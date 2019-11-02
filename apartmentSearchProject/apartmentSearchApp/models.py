from django.db import models

# Create your models here.

# class Address(models.Model):
#     line_1 = models.CharField(max_length=100)
#     line_2 = models.CharField(max_length=100, null=True)
#     city = models.CharField(max_length=100, default='Columbus')
#     state = models.CharField(max_length=100, default='Ohio')
#     country = models.CharField(max_length=100, default='United States')
#     zip_code = models.PositiveIntegerField()

class Listing(models.Model):
    AREA_CHOICES = [('N', 'North Campus'), ('S', 'South Campus')]

    price = models.PositiveIntegerField(null=True)
    # address = models.OneToOneField(Address, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.FloatField()
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    miles_from_campus = models.FloatField(null=True)
    area_of_campus = models.CharField(max_length=10, choices=AREA_CHOICES)
    url = models.CharField(max_length=1000)
    availability_date = models.DateField(null=True)
    active = models.BooleanField()

    listings = models.Manager()