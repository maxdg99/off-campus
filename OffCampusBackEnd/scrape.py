from bs4 import BeautifulSoup
import requests
import base64
import json, sys
from urllib.parse import urljoin
from OffCampusRestApi.models import Listing
from OffCampusWebScrapers.scraper import Scraper
from OffCampusWebScrapers.appfolio import *
from OffCampusWebScrapers.pella import PellaScraper
from OffCampusWebScrapers.hometeam import HometeamScraper
from OffCampusWebScrapers.peak import PeakScraper
from OffCampusWebScrapers.osu_properties import OSUPropertiesScraper
from OffCampusWebScrapers.krg import KRGScraper
from OffCampusBackEnd.utility import getLatLong, distance, standardize_address
import os, sys
from PIL import Image
from OffCampusBackEnd.settings import STATIC_DISK_LOCATION, STATIC_URL

options = [cls for cls in Scraper.__subclasses__()]

print("Available classnames: "+str(options))

def insert_listing_from_dict(l):
    string_address, tokenized_address = standardize_address(l["address"])
    try:
        obj = Listing.listings.get(address=string_address)
        print("exists: "+string_address)

        l["address"] = string_address
        for attr, value in tokenized_address.items():
            l[attr] = value

        # Set updated date
        obj.date_updated = datetime.datetime.now().date()

        for key, value in l.items():
            setattr(obj, key, value)

        if l["price"] != None and int(l["price"]) > 0:
            obj.save()
    except Listing.DoesNotExist:
        print("inserting: "+string_address)

        # Get lat long
        l["latitude"], l["longitude"] = getLatLong(string_address)

        if l["latitude"] is not None:
            l["miles_from_campus"] = round(distance(l["latitude"], l["longitude"]), 2)
            print("\t\tDistance: "+str(distance(l["latitude"], l["longitude"])))

        l["address"] = string_address
        for attr, value in tokenized_address.items():
            l[attr] = value

        obj = Listing(**l)

        # Set created date
        obj.date_created = datetime.datetime.now().date()
        obj.date_updated = obj.date_created

        if l["price"] != None and int(l["price"]) > 0:
            obj.save()

        image_path = os.path.join(STATIC_DISK_LOCATION, f"images/{obj.id}.png")
        image_url = os.path.join(STATIC_URL, f"images/{obj.id}.png")

        response = requests.get(obj.image)
        file = open(image_path, "wb")
        file.write(response.content)

        # Get the size in MB of the file without resizing
        file_size = os.stat(image_path).st_size / 1000000

        file.close()

        # If the file is bigger than 1 MB, we should resize it and store it.
        if file_size > 1:
            obj.image = image_url
            obj.save()

            image = Image.open(image_path)
            image.thumbnail((300, 300))
            image.save(image_path)
        else:
            os.remove(image_path)

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

