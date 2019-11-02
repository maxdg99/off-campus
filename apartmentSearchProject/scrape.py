from bs4 import BeautifulSoup
import requests
import base64
import json
from urllib.parse import urljoin
from apartmentSearchApp.models import Listing
from scrapers.scraper import Scraper
from scrapers.hometeam import HometeamScraper
from scrapers.northsteppe import NorthsteppeScraper

options = [cls for cls in Scraper.__subclasses__()]

print(options)


def insert_listing_from_dict(l):
    try:
        obj = Listing.listings.get(address=l["address"])
        print("exists: "+l["address"])
        for key, value in l.items():
            setattr(obj, key, value)
        obj.save()
    except Listing.DoesNotExist:
        print("inserting: "+l["address"])
        obj = Listing(**l)
        obj.save()

    except Listing.MultipleObjectsReturned:
        print("multiple returned for: "+l["address"])


for o in options:
    o.process_listings(insert_listing_from_dict)
    
