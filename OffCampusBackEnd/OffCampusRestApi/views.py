from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from OffCampusRestApi.models import Listing
from OffCampusRestApi.models import GoogleUser
from OffCampusRestApi.compute_averages import compute_averages
from google.oauth2 import id_token
from google.auth.transport import requests
import json
orderOptions = [{'id': '1', 'text': 'Price Increasing'}, {'id': '2', 'text': 'Price Decreasing'}, {'id': '3', 'text': 'Distance Increasing'}, {'id': '4', 'text': 'Distance Decreasing'}]
orderQueries = {'1': 'price', '2': '-price', '3': 'miles_from_campus', '4': '-miles_from_campus'}

orderOptions = [{'id': '1', 'text': 'Price Increasing'}, {'id': '2', 'text': 'Price Decreasing'}, {'id': '3', 'text': 'Distance Increasing'}, {'id': '4', 'text': 'Distance Decreasing'}]
areaOptions = [{'name': "Any", 'code': ""}, {'name': "North", 'code': "north"}, {'name': "South", 'code': "south"}, {'name': "Northwest", 'code': "northwest"}, {'name': "Northeast", 'code': "northeast"}, {'name': "Southwest", 'code': "southwest"}, {'name': "Southeast", 'code': "southeast"}]
areaOptionsKeys = list(map(lambda x: x['code'], areaOptions))
areaOptionsKeys.remove('')
orderQueries = {'1': 'price', '2': '-price', '3': 'miles_from_campus', '4': '-miles_from_campus'}

averages = None

def getSearchListingsPage(request):
    global averages # This is necessary
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

    return {"page_count": paginator.num_pages, "listings": list(listingsPage), "result_count": len(listings)}

def likeProperty(request):
    data = {}
    property_id = None

    if 'property_id' in request.GET:
        property_id = request.GET['property_id']

    if request.session.has_key('offcampus.us_auth'):
        row = request.session.get('offcampus.us_auth')
        user = GoogleUser.objects.get(pk=row)
        favorites = user.favorites.all()
        try:
            listing = Listing.listings.get(id=property_id)
            user.favorites.add(listing)
            response = JsonResponse(status=200, data=data)
        except Listing.DoesNotExist:
            # Fail because this means the listing does not exist
            response = HttpResponse(status=404)    
    else:
        # This means the user is not logged in
        response = HttpResponse(status=401)
    __allowCors(response)
    return response
        
def unlikeProperty(request):
    data = {}
    property_id = None

    if 'property_id' in request.GET:
        property_id = request.GET['property_id']

    if request.session.has_key('offcampus.us_auth') and property_id:
        row = request.session.get('offcampus.us_auth')
        user = GoogleUser.objects.get(pk=row)
        favorites = user.favorites.all()
        if Listing.listings.filter(id=property_id).exists():
            listing = Listing.listings.get(id=property_id)
            user.favorites.remove(listing)
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
    listings = __getFilteredListings(request)
    response = JsonResponse(list(listings), safe=False)
    __allowCors(response)
    return response

def getLikedListings(request):
    if 'offcampus.us_auth' in request.session:
        row = request.session.get('offcampus.us_auth')
        listings = GoogleUser.objects.get(pk=row).favorites.values_list('pk', flat=True)
        data =  list(listings)
        response = JsonResponse(data=data, content_type="application/json", status=200, safe=False)
        __allowCors(response)
        return response
    else:
        response = HttpResponse(status=401)
        return response

@csrf_exempt
def sign_in(request):
    if request.POST:
        return __google_sign_in(request)
    else:
        return HttpResponse(status=400)

def isSignedIn(request):
    data = {}
    data["isSignedIn"] = request.session.has_key('offcampus.us_auth')
    response = JsonResponse(data)
    __allowCors(response)
    return response
    
def sign_out(request):
    request.session.flush()
    request.session.modified = True
    response = HttpResponse(status=201)
    __allowCors(response)
    return response

def getOrderOptions(request):
    response = JsonResponse(orderOptions, safe=False)
    __allowCors(response)
    return response

def getAreaOptions(request):
    response = JsonResponse(areaOptions, safe=False)
    __allowCors(response)
    return response

def __google_sign_in(request):
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
            if not GoogleUser.objects.filter(google_id=user_id).exists():
                user = GoogleUser(google_id=user_id)
                user.save()
            request.session['offcampus.us_auth'] = GoogleUser.objects.get(google_id=user_id).pk
            response = HttpResponse(status=201)
        __allowCors(response)
        request.session.modified = True
        return response

def __allowCors(response):
    print("allow CORS")
    response["Access-Control-Allow-Origin"] = "http://localhost:8080"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    response["Access-Control-Allow-Credentials"] = 'true'

def __getFilteredListings(request):
    queryParams = request.GET

    if not ("showOnlyLiked" in queryParams and queryParams["showOnlyLiked"] == "true"):
        listingsFilter = Q(active=True)
    else:
        listingsFilter = Q()

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
    if "minDistance" in queryParams:
        try:
            minDistanceFloat = float(queryParams["minDistance"])
            listingsFilter = listingsFilter & Q(miles_from_campus__gte=minDistanceFloat)
        except ValueError:
            pass
    if "maxDistance" in queryParams:
        try:
            maxDistanceFloat = float(queryParams["maxDistance"])
            listingsFilter = listingsFilter & Q(miles_from_campus__lte=maxDistanceFloat)
        except ValueError:
            pass

    if "campus_area" in queryParams and queryParams["campus_area"] in areaOptionsKeys:
        listingsFilter = listingsFilter & Q(campus_area=queryParams["campus_area"])

    listings = Listing.listings.all()

    print(request.session.get('offcampus.us_auth'))
    if "showOnlyLiked" in queryParams and queryParams["showOnlyLiked"] == "true" and request.session.has_key('offcampus.us_auth'):
        row = request.session.get('offcampus.us_auth')
        print("SHOWING LIKES")
        listings = GoogleUser.objects.get(pk=row).favorites.all()

    # Parses ordering of listings
    if "order" in queryParams:
        if queryParams["order"] in orderQueries:
            return listings.filter(listingsFilter).order_by(orderQueries[queryParams["order"]]).values('address', 'active', 'availability_date', 'availability_mode', 'beds', 'baths', 'campus_area', 'image', 'latitude', 'longitude', 'price', 'url', 'pk', 'miles_from_campus')
        else:
            # Default order is miles from campus, increasing
            return listings.filter(listingsFilter).order_by(orderQueries['3']).values('address', 'active', 'availability_date', 'availability_mode', 'beds', 'baths', 'campus_area', 'image', 'latitude', 'longitude', 'price', 'url', 'pk', 'miles_from_campus')
