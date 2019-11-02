from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from apartmentSearchApp.models import Listing

# Create your views here.
def index(request):
    listings = Listing.listings.all()
    context = { 'listings': listings }
    return render(request, 'index.html', context)

def banana(request):
    l = Listing()
    l.latitude = 40.006150
    l.longitude = -83.010930
    l.price = 69
    l.address = '420 W Lane Ave'
    l.num_bedrooms = 3
    l.num_bathrooms = 0.5
    l.active = True
    l.save()
    return HttpResponse('<b>Yeehaw</b><br><img src="https://media1.giphy.com/media/IB9foBA4PVkKA/giphy.gif">')
