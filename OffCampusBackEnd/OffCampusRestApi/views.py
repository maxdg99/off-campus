from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from OffCampusRestApi.models import Listing
from OffCampusRestApi.models import User
from OffCampusRestApi.compute_averages import compute_averages
import json

orderOptions = [{'id': '1', 'text': 'Price Increasing'}, {'id': '2', 'text': 'Price Decreasing'}, {'id': '3', 'text': 'Distance Increasing'}, {'id': '4', 'text': 'Distance Decreasing'}]
orderQueries = {'1': 'price', '2': '-price', '3': 'miles_from_campus', '4': '-miles_from_campus'}

averages = None

def getSearchListingsPage(request):
    listingsPage = __getPaginatedListings(request)
    if not averages:
        averages = compute_averages()

    for listing in listingsPage["listings"]:
        if listing.price is not None:
            avg = averages[(listing.beds, listing.baths)]
            listing.diff_raw = listing.price - avg
            listing.percent_diff = f"{(listing.price - avg) / avg * 100:+.0f}"

    context = { 'listings': listingsPage, 'averages': averages}
    return render(request, 'index.html', context)


def getPaginatedListings(request):
    queryResult = __getPaginatedListings(request)
    queryResult["listings"] = json.loads(serializers.serialize('json', queryResult["listings"])) # this is dumb-af but it's what i gotta do
    response = JsonResponse(queryResult)
    __allowCors(response)
    return response


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

    return {"page_count": paginator.num_pages, "listings": listingsPage, "result_count": len(listings)}

def getAllListings(request):
    listings = __getFilteredListings(request)
    response = HttpResponse(serializers.serialize('json', listings), content_type="application/json")
    __allowCors(response)
    return response

def getOrderOptions(request):
    response = JsonResponse(orderOptions, safe=False)
    __allowCors(response)
    return response

def __allowCors(response):
    print("allow CORS")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"


def __getFilteredListings(request):
    queryParams = request.GET
    listingsFilter = Q(active=True)

    # Parses beds and baths
    if "beds" in queryParams and queryParams["beds"].isnumeric():
        listingsFilter = listingsFilter & Q(beds=queryParams["beds"])
    if "baths" in queryParams and queryParams["baths"].isnumeric():
        listingsFilter = listingsFilter & Q(baths=queryParams["baths"])

    secondaryListingsFilter = Q()

    # Parses minimum and maximum price
    if "minPrice" in queryParams and queryParams["minPrice"].isnumeric():
        secondaryListingsFilter = secondaryListingsFilter & Q(price__gte=queryParams["minPrice"])
    if "maxPrice" in queryParams and queryParams["maxPrice"].isnumeric():
        secondaryListingsFilter = secondaryListingsFilter & Q(price__lte=queryParams["maxPrice"])

    # Only show listings with prices
    secondaryListingsFilter = secondaryListingsFilter & Q(price__isnull=False)

    listingsFilter = listingsFilter & secondaryListingsFilter

    # Parses minimum and maximum distances from campus
    if "minDistance" in queryParams and queryParams["minDistance"].isnumeric():
        listingsFilter = listingsFilter & Q(miles_from_campus__gte=queryParams["minDistance"])
    if "maxDistance" in queryParams and queryParams["maxDistance"].isnumeric():
        listingsFilter = listingsFilter & Q(miles_from_campus__lte=queryParams["maxDistance"])

    # Parses ordering of listings
    if "order" in queryParams:
        if queryParams["order"] in orderQueries:
            return Listing.listings.filter(listingsFilter).order_by(orderQueries[queryParams["order"]])
        else:
            # Default order is miles from campus, increasing
            return Listing.listings.filter(listingsFilter).order_by(orderQueries['3'])
