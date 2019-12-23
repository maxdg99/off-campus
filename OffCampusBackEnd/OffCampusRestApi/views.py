from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from OffCampusRestApi.models import Listing
from OffCampusRestApi.models import User
from OffCampusRestApi.compute_averages import compute_averages
from apiclient import discovery
import httplib2
from oauth2client import client
from google.oauth2 import id_token
from google.auth.transport import requests
import json

averages = None

def getSearchListingsPage(request):
    global averages # This is necessary
    listingsPage = __getPaginatedListings(request)
    if not averages:
        averages = compute_averages()

    for listing in listingsPage["listings"]:
        if listing.price is not None:
            avg = averages[(listing.num_bedrooms, listing.num_bathrooms)]
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

    return {"page_count": paginator.num_pages, "listings": listingsPage}
# Should this be GET or POST. Is POST more secure when dealing with id tokens?
def isLikedProperty(request):
    print(request.GET)
    request_data = request.GET
    token = request_data['id_token']
    property_id = request_data['property_id']
    user_id = None

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        user_id = idinfo['sub']
    except ValueError:
        pass

    data = {}
    if user_id:
        if User.objects.filter(google_id=user_id).exists() and Listing.listings.get(id=property_id) in User.objects.get(google_id=user_id).favorites.all():
            data["isLiked"] = True
        else:
            data["isLiked"] = False
    else:
        data["isLiked"] = False
    response = JsonResponse(data)
    __allowCors(response)
    return response

@csrf_exempt 
def toggleLikedProperty(request):
    request_data = request.POST
    token = request_data['id_token']
    property_id = request_data['property_id']
    user_id = None
    response = HttpResponse(status=201)
    data = {}

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        user_id = idinfo['sub']
    except ValueError:
        pass

    if user_id:
        if not User.objects.filter(google_id=user_id).exists():
            user = User(google_id=user_id)
            user.save()
        else:
            user = User.objects.get(google_id=user_id)

        favorites = user.favorites.all()

        if Listing.listings.filter(id=property_id).exists():
            listing = Listing.listings.get(id=property_id)
            if listing in favorites:
                user.favorites.remove(listing)
                data["isLiked"] = False
            else:
                user.favorites.add(listing)
                data["isLiked"] = True
            response = JsonResponse(data)
        else:
            response = HttpResponse(status=404)    
    else:
        response = HttpResponse(status=404)
    __allowCors(response)
    return response

def getAllListings(request):
    listings = Listing.listings.all()
    response = HttpResponse(serializers.serialize('json', listings), content_type="application/json")
    __allowCors(response)
    return response

def __allowCors(response):
    response["Access-Control-Allow-Origin"] = "http://localhost:8080" #must be the url of the website
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "x-requested-with, Content-Type"


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