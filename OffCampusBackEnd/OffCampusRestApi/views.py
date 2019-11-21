from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from OffCampusRestApi.models import Listing
from OffCampusRestApi.models import User
from OffCampusRestApi.compute_averages import compute_averages
from apiclient import discovery
import httplib2
from oauth2client import client

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

def isSignedIn(request):
    response = {}
    if 'offcampus.us_auth' in request and Users.id.find(id=request.session['offcampus.us_auth']).exists():
        response["signedIn"] = True
    else:
        response["signedIn"] = False
    return HttpResponse(serializers.serialize('json', response), content_type="application/json")

def signOut(request):
    if request.session['offcampus.us_auth'] != None:
        request.session.flush()

def authorizeUser(request):

    if not request.headers.get('X-Requested-With'):
        abort(403)

    CLIENT_SECRET_FILE = './client_secret.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
        auth_code)

    # Call Google API
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http_auth)
    appfolder = drive_service.files().get(fileId='appfolder').execute()

    # Get profile info from ID token
    user_id = credentials.id_token['sub']

    if not User.google_id.filter(google_id=user_id).exists():
        # Save the user's info in database
        new_user = User(google_id=user_id)
        new_user.save()

    user = User.google_id.filter(google_id=user_id)

    response = HttpResponse('Success')
    request.session['offcampus.us_auth'] = user.id

    return response

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