from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db.models import Q

from apartmentSearchApp.models import Listing

# Create your views here.
def index(request):
    query = request.GET
    # beds baths minPrice maxPrice showNoPrice minDistance maxDistance
    varargs = {}
    q = Q()
    if "beds" in query:
        q = q & Q(num_bedrooms=query["beds"])
    if "baths" in query:
        q = q & Q(num_bathrooms=query["baths"])

    
    q1 = Q()
    if "minPrice" in query:
        q1 = q1 & Q(price__gte=query["minPrice"])
    if "maxPrice" in query:
        q1 = q1 & Q(price__lte=query["maxPrice"])

    if "showNoPrice" in query:
        if query["showNoPrice"] != "off":
            q1 = q1 | Q(price__isnull=True)
        else:
            q1 = q1 & Q(price__isnull=False)


    q = q & q1

    if "minDistance" in query:
        q = q & Q(miles_from_campus__gte=query["minDistance"])
    if "maxDistance" in query:
        q = q & Q(miles_from_campus__lte=query["maxDistance"])

    listings = Listing.listings.filter(q)

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
