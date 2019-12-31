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

def toggleLikedProperty(request):
    property_id = request.GET['property_id']
    data = {}

    if request.session.has_key('offcampus.us_auth'):
        row = request.session.get('offcampus.us_auth')
        user = User.objects.get(pk=row)
        favorites = user.favorites.all()
        if Listing.listings.filter(id=property_id).exists():
            listing = Listing.listings.get(id=property_id)
            if listing in favorites:
                user.favorites.remove(listing)
                data["isLiked"] = False
            else:
                user.favorites.add(listing)
                data["isLiked"] = True
            response = JsonResponse(status=200, data=data)
        else:
            # Fail because this means the listing does not exist
            response = HttpResponse(status=404)    
    else:
        # This means the user is not logged in
        response = HttpResponse(status=401)
    __allowCors(response)
    return response

def getAllListings(request):
    listings = Listing.listings.all()
    response = HttpResponse(serializers.serialize('json', listings), content_type="application/json")
    __allowCors(response)
    return response

def getLikedListings(request):
    row = request.session.get('offcampus.us_auth')
    if 'offcampus.us_auth' in request.session:
        listings = User.objects.get(pk=row).favorites.values_list('pk', flat=True)
        data =  list(listings)
        response = JsonResponse(data=data, content_type="application/json", status=200, safe=False)
        __allowCors(response)
        return response
    else:
        response = HttpResponse(status=401)
        return response

@csrf_exempt
def login(request):
    if request.POST:
        token = request.POST.get('id_token')
        user_id = None
        response = HttpResponse(status=404)
        if token:
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
                request.session['offcampus.us_auth'] = User.objects.get(google_id=user_id).pk
                response = HttpResponse(status=201)
        __allowCors(response)
        request.session.modified = True
        return response
    else:
        return HttpResponse(status=400)

def isSignedIn(request):
    data = {}
    data["isSignedIn"] = request.session.has_key('offcampus.us_auth')
    response = JsonResponse(data)
    __allowCors(response)
    return response
    
def logout(request):
    request.session.flush()
    response = HttpResponse(status=201)
    __allowCors(response)
    return response

def __allowCors(response):
    response["Access-Control-Allow-Origin"] = "http://localhost:8080" #must be the url of the website
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "x-requested-with, Content-Type"
    response["Access-Control-Allow-Credentials"] = 'true'

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

    listings = Listing.listings.all()

    if "showOnlyLiked" in queryParams and queryParams["showOnlyLiked"] == "true" and request.session.has_key('offcampus.us_auth'):
        row = request.session.get('offcampus.us_auth')
        listings = User.objects.get(pk=row).favorites.all()

    # Parses ordering of listings
    if "order" in queryParams:
        if queryParams["order"] == "price_increasing":
            return listings.filter(listingsFilter).order_by('price')
        elif queryParams["order"] == "price_decreasing":
            return listings.filter(listingsFilter).order_by('-price')
        elif queryParams["order"] == "distance_decreasing":
            return listings.filter(listingsFilter).order_by('-miles_from_campus')

    # Default order is miles from campus, increasing
    return listings.filter(listingsFilter).order_by('miles_from_campus')