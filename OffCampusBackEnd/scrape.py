from bs4 import BeautifulSoup
import requests
import base64
import json, sys
from urllib.parse import urljoin
from OffCampusRestApi.models import Listing
from OffCampusWebScrapers.scraper import Scraper
from OffCampusWebScrapers.appfolio import *
from OffCampusWebScrapers.pella import PellaScraper
from OffCampusWebScrapers.eventide import EventideScraper
from OffCampusWebScrapers.hometeam import HometeamScraper
from OffCampusWebScrapers.peak import PeakScraper
from OffCampusWebScrapers.osu_properties import OSUPropertiesScraper
from OffCampusWebScrapers.krg import KRGScraper
from OffCampusBackEnd.utility import getLatLong, distance, standardize_address, get_region
import os, sys
from PIL import Image
from OffCampusBackEnd.settings import STATIC_BASE, STATIC_DISK_LOCATION
from urllib.parse import urlparse
options = [cls for cls in Scraper.__subclasses__()]

print("Available classnames: "+str(options))

scrape_count =0
def insert_listing_from_dict(l):
    global scrape_count
    scrape_count += 1
    string_address, tokenized_address = standardize_address(l["address"])
    try:
        obj = Listing.listings.get(address=string_address)
        
        if obj.scraper != l["scraper"]:
            print("MISMATCH: "+string_address)
            print(obj.scraper+" vs. new "+l["scraper"])
        
        #print("exists: "+string_address)
        print(".", end="", flush=True)

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
        #print("inserting: "+string_address)
        print("+", end="", flush=True)

        # Get lat long
        l["latitude"], l["longitude"] = getLatLong(string_address)

        if l["latitude"] is not None:
            l["miles_from_campus"] = round(distance(l["latitude"], l["longitude"]), 2)
            l['campus_area'] = get_region(l['latitude'], l["longitude"])
            #print("\t\tDistance: "+str(distance(l["latitude"], l["longitude"])))
            #print("\t\tRegion: "+l['campus_area'])


        l["address"] = string_address
        for attr, value in tokenized_address.items():
            l[attr] = value

        obj = Listing(**l)

        # Set created date
        obj.date_created = datetime.datetime.now().date()
        obj.date_updated = obj.date_created

        # Update image path to use HTTPS
        parsed_image_url = urlparse(obj.image)
        if parsed_image_url.hostname != "pellaco.com":
            parsed_image_url = parsed_image_url._replace(scheme="https")
            obj.image = parsed_image_url.geturl()

        if l["price"] != None and int(l["price"]) > 0:
            obj.save()

        if len(parsed_image_url.netloc) > 0:
            # Download the image to get a sense of the size
            image_path = os.path.join(STATIC_DISK_LOCATION, f"images/{obj.id}.png")
            image_url = os.path.join(STATIC_BASE, f"images/{obj.id}.png")

            headers = requests.head(obj.image)
            if int(headers.headers["content-length"]) > 1000000:
                # Create a thumbnail version of the image
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
    global scrape_count
    if classnames is None:
        classes = options
        Listing.listings.all().update(active=False)
    else:
        classes = []
        for x in classnames:
            classes.append(getattr(sys.modules[__name__], x))
        Listing.listings.filter(scraper__in=classnames).update(active=False)
    for o in classes:
        scrape_count = 0
        print(o.__name__+": ")
        try:
            o.process_listings(insert_listing_from_dict)
            print("\nSuccessfully scraped: "+str(scrape_count))
        except Exception as e:
            print("Error on property "+str(scrape_count))
            print("/n")
            print("ERROR IN SCRAPER.")
            print(e)
            print("CLASS " + o.__name__ + " IS FAILING")
        

