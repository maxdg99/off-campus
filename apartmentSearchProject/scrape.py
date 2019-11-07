from bs4 import BeautifulSoup
import requests
import base64
import json
from urllib.parse import urljoin
from apartmentSearchApp.models import Listing
from scrapers.scraper import Scraper
from scrapers.appfolio import BuckeyeScraper # this imports all of the appfolio scrapers idk why
from scrapers.pella import PellaScraper

from apartmentSearchProject.utility import getLatLong, distance

options = [cls for cls in Scraper.__subclasses__()]

print(options)


def insert_listing_from_dict(l):
    try:
        obj = Listing.listings.get(address=l["address"])
        print("exists: "+l["address"])

        if (obj.latitude is None):
            # Get lat long
            l["latitude"], l["longitude"] = getLatLong(l["address"])
            print(f'{l["latitude"]} {l["longitude"]}')
        else:
            obj.miles_from_campus = round(distance(obj.latitude, obj.longitude), 2)
            print("\t\tDistance: "+str(distance(obj.latitude, obj.longitude)))

        for key, value in l.items():
            setattr(obj, key, value)
        obj.save()
    except Listing.DoesNotExist:
        print("inserting: "+l["address"])

        # Get lat long
        l["latitude"], l["longitude"] = getLatLong(l["address"])
        print(f'{l["latitude"]} {l["longitude"]}')

        if l["latitude"] is not None:
            obj.miles_from_campus = round(distance(obj["latitude"], obj["longitude"]), 2)
            print("\t\tDistance: "+str(distance(obj["latitude"], obj["longitude"])))

        obj = Listing(**l)
        obj.save()

    except Listing.MultipleObjectsReturned:
        print("multiple returned for: "+l["address"])


for o in options:
    o.process_listings(insert_listing_from_dict)
    
