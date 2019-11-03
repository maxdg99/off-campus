from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


from apartmentSearchApp.models import Listing
from apartmentSearchApp.compute_averages import compute_averages

averages = compute_averages()

def query_for_request(request):
    query = request.GET
    # beds baths minPrice maxPrice showNoPrice minDistance maxDistance
    varargs = {}
    q = Q()
    if "beds" in query and query["beds"].isnumeric():
        q = q & Q(num_bedrooms=query["beds"])

    if "baths" in query and query["baths"].isnumeric():
        q = q & Q(num_bathrooms=query["baths"])

    
    q1 = Q()
    price_constrained = False
    if "minPrice" in query and query["minPrice"].isnumeric():
        q1 = q1 & Q(price__gte=query["minPrice"])
        price_constrained = True
    if "maxPrice" in query and query["maxPrice"].isnumeric():
        q1 = q1 & Q(price__lte=query["maxPrice"])
        price_constrained = True

    if "showNoPrice" in query and query["showNoPrice"] == "false":
        q1 = q1 & Q(price__isnull=False)
    elif price_constrained:
        q1 = q1 | Q(price__isnull=True)
    
    q = q & q1

    if "minDistance" in query and query["minDistance"].isnumeric():
        q = q & Q(miles_from_campus__gte=query["minDistance"])
    if "maxDistance" in query and query["maxDistance"].isnumeric():
        q = q & Q(miles_from_campus__lte=query["maxDistance"])

    if "order" in query:
        if query["order"] == "price_increasing":
            return Listing.listings.filter(q).order_by('price')
        elif query["order"] == "price_decreasing":
            return Listing.listings.filter(q).order_by('-price')
        elif query["order"] == "distance_decreasing":
            return Listing.listings.filter(q).order_by('-miles_from_campus')
    
    # default is order by miles from campus, increasing
    return Listing.listings.filter(q).order_by('miles_from_campus')

# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    listings_list = query_for_request(request)
    paginator = Paginator(listings_list, 20)

    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    for x in listings:
        if x.price is None:
            continue
        avg = averages[(x.num_bedrooms, x.num_bathrooms)]
        x.diff_raw = x.price - avg
        x.percent_diff = f"{(x.price - avg) / avg * 100:+.0f}"

    context = { 'listings': listings, 'averages': averages, 'paginator': paginator}
    return render(request, 'index.html', context)

def query_json(request):
    results = query_for_request(request)
    
    return HttpResponse(serializers.serialize('json', results), content_type="application/json")

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
