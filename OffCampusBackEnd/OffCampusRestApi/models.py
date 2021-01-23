from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils.translation import gettext_lazy as _

class Listing(models.Model):

    class AvailabilityMode(models.TextChoices):
        SEASON = 'S', _('Season')
        MONTH = 'M', _('Month')
        NOW = 'N', _('Now')
        NONE = '-', _('None')
        DATE = 'D', _('Date')

    class CampusArea(models.TextChoices):
        NORTH = 'north', _('North Campus')
        NORTHEAST = 'northeast', _('Northeast Campus')
        NORTHWEST = 'northwest', _('Northwest Campus')
        SOUTH = 'south', _('South Campus')
        SOUTHEAST = 'southeast', _('Southeast Campus')
        SOUTHWEST = 'southwest', _('Southwest Campus')

    url = models.CharField(max_length=1000)
    
    image = models.CharField(max_length=1000)
    
    address = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10, default="")
    street_range = models.CharField(max_length=25, default="")
    street_prefix = models.CharField(max_length=10, default="")
    street_name = models.CharField(max_length=50, default="")
    street_type = models.CharField(max_length=10, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=5, default="")
    zipcode = models.CharField(max_length=5, default="")
    unit = models.CharField(max_length=10, default="")

    campus_area = models.CharField(max_length=10, choices=CampusArea.choices)

    beds = models.PositiveIntegerField(null=True)
    baths = models.FloatField(null=True)

    description = models.CharField(max_length=1000, default="")

    price = models.PositiveIntegerField(null=True)

    availability_date = models.DateField(null=True)
    availability_mode = models.CharField(max_length=2, choices=AvailabilityMode.choices, default=AvailabilityMode.NONE)
    active = models.BooleanField()

    date_created = models.DateField()
    date_updated = models.DateField()

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    
    miles_from_campus = models.FloatField(null=True)
    
    scraper = models.CharField(max_length=100)

    percent_diff = None # populated at runtime
    diff_raw = 0

    listings = models.Manager()

class GoogleUser(models.Model):
    google_id = models.CharField(max_length=255)
    favorites = models.ManyToManyField(Listing) 