from bs4 import BeautifulSoup
import requests
import base64
import json, sys
from urllib.parse import urljoin
from OffCampusRestApi.models import Listing
from OffCampusWebScrapers.scraper import Scraper
from OffCampusWebScrapers.appfolio import *
from OffCampusWebScrapers.pella import PellaScraper
# from OffCampusWebScrapers.eventide import EventideScraper
from OffCampusWebScrapers.hometeam import HometeamScraper
from OffCampusWebScrapers.peak import PeakScraper
# cfrom OffCampusWebScrapers.cooper import CooperScraper

from OffCampusBackEnd.utility import getLatLong, distance

options = [cls for cls in Scraper.__subclasses__()]

print("Available classnames: "+str(options))

def insert_listing_from_dict(l):
    try:
        obj = Listing.listings.get(address=l["address"])
        print("exists: "+l["address"])

        # Set updated date
        obj.date_updated = datetime.datetime.now().date()
        
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
            l["miles_from_campus"] = round(distance(l["latitude"], l["longitude"]), 2)
            print("\t\tDistance: "+str(distance(l["latitude"], l["longitude"])))

        obj = Listing(**l)

        # Set created date
        obj.date_created = datetime.datetime.now().date()
        obj.date_updated = obj.date_created

        obj.save()

    except Listing.MultipleObjectsReturned:
        print("multiple returned for: "+l["address"])


def scrape(classnames=None):
    if classnames is None:
        classes = options
        Listing.listings.all().update(active=False)
    else:
        classes = []
        for x in classnames:
            classes.append(getattr(sys.modules[__name__], x))
        Listing.listings.filter(scraper__in=classnames).update(active=False)
    for o in classes:
        o.process_listings(insert_listing_from_dict)
    
