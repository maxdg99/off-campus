from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from OffCampusRestApi.models import Listing
from OffCampusRestApi.compute_averages import compute_averages

averages = compute_averages()


def getSearchListingsPage(request):
    listingsPage = __getPaginatedListings(request)

    for listing in listingsPage:
        if listing.price is not None:
            avg = averages[(listing.num_bedrooms, listing.num_bathrooms)]
            listing.diff_raw = listing.price - avg
            listing.percent_diff = f"{(listing.price - avg) / avg * 100:+.0f}"

    context = { 'listings': listingsPage, 'averages': averages}
    return render(request, 'index.html', context)


def getPaginatedListings(request):
    listings = __getPaginatedListings(request)
    return HttpResponse(serializers.serialize('json', listings), content_type="application/json")


# TODO: change page to pageNumber and add pageSize query parameter
def __getPaginatedListings(request):
    page = request.GET.get('page', 1)
    listings = __getFilteredListings(request)
    paginator = Paginator(listings, 20)
    
    try:
        listingsPage = paginator.page(page)
    except PageNotAnInteger:
        listingsPage = paginator.page(1)
    except EmptyPage:
        listingsPage = paginator.page(paginator.num_pages)

    return listingsPage


def getAllListings(request):
    listings = Listing.listings.all()
    return HttpResponse(serializers.serialize('json', listings), content_type="application/json")


def __getFilteredListings(request):
    queryParams = request.GET
    listingsFilter = Q(active=True)

    # Parses beds and baths
    if "beds" in queryParams and queryParams["beds"].isnumeric():
        listingsFilter = listingsFilter & Q(num_bedrooms=queryParams["beds"])
    if "baths" in queryParams and queryParams["baths"].isnumeric():
        listingsFilter = listingsFilter & Q(num_bathrooms=queryParams["baths"])

    secondaryListingsFilter = Q()
    price_constrained = False

    # Parses minimum and maximum price
    if "minPrice" in queryParams and queryParams["minPrice"].isnumeric():
        secondaryListingsFilter = secondaryListingsFilter & Q(price__gte=queryParams["minPrice"])
        price_constrained = True
    if "maxPrice" in queryParams and queryParams["maxPrice"].isnumeric():
        secondaryListingsFilter = secondaryListingsFilter & Q(price__lte=queryParams["maxPrice"])
        price_constrained = True

    # Parses showing listings without prices
    if "showNoPrice" in queryParams and queryParams["showNoPrice"] == "false":
        secondaryListingsFilter = secondaryListingsFilter & Q(price__isnull=False)
    elif price_constrained:
        secondaryListingsFilter = secondaryListingsFilter | Q(price__isnull=True)
    
    listingsFilter = listingsFilter & secondaryListingsFilter

    # Parses minimum and maximum distances from campus
    if "minDistance" in queryParams and queryParams["minDistance"].isnumeric():
        listingsFilter = listingsFilter & Q(miles_from_campus__gte=queryParams["minDistance"])
    if "maxDistance" in queryParams and queryParams["maxDistance"].isnumeric():
        listingsFilter = listingsFilter & Q(miles_from_campus__lte=queryParams["maxDistance"])

    # Parses ordering of listings
    if "order" in queryParams:
        if queryParams["order"] == "price_increasing":
            return Listing.listings.filter(listingsFilter).order_by('price')
        elif queryParams["order"] == "price_decreasing":
            return Listing.listings.filter(listingsFilter).order_by('-price')
        elif queryParams["order"] == "distance_decreasing":
            return Listing.listings.filter(listingsFilter).order_by('-miles_from_campus')
    
    # Default order is miles from campus, increasing
    return Listing.listings.filter(listingsFilter).order_by('miles_from_campus')