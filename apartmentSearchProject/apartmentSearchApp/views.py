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
    l.price = 42069
    l.address = '42069 W. Lane Ave'
    l.num_bedrooms = 3
    l.num_bathrooms = 0.5
    l.active = True
    l.save()
    return HttpResponse('<b>Yeehaw</b><img src="https://yt3.ggpht.com/a/AGF-l786UWF6pmeRZI5z8V1lFYr4MFI2RQhyh24vZA=s900-c-k-c0xffffffff-no-rj-mo">')
