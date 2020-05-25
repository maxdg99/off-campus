from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils.translation import gettext_lazy as _

class Listing(models.Model):
    AVAILABILITY_MODE = [('S', 'Season'), ('M', 'Month'), ('N', 'Now'), ('-', 'None'), ('D', 'Date')]
    url = models.CharField(max_length=1000)
    
    image = models.CharField(max_length=1000)
    
    pretty_address = models.CharField(max_length=100)
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
    
    scraper = models.CharField(max_length=100)

    percent_diff = None # populated at runtime
    diff_raw = 0

    listings = models.Manager()

class User(AbstractBaseUser):
    class SocialAccount(models.TextChoices):
        Google = 'G', _('Google')
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    password = models.CharField(max_length=100)
    social_account_id = models.CharField(max_length=2, choices=SocialAccount.choices)
    favorites = models.ManyToManyField(Listing, through="Favorite")

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    note = models.CharField(max_length=1000)
    rating = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])