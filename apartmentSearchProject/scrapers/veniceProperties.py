# Imports
from bs4 import BeautifulSoup
import requests
from scrapers.scraper import Scraper
import datetime

class VenicePropertiesScraper(Scraper):

    # URL of all properties
    venicePropertiesUrl = "https://veniceprops.appfolio.com/listings/listings"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Parses listings from page
    def process_listings(callback):
        # Retrieves all information for webpage
        ns = requests.get(url=VenicePropertiesScraper.venicePropertiesUrl, headers=VenicePropertiesScraper.headers)
        # Pulls out just the HTML Template
        nsHTML = ns.text
        # Create an HTML Scraper for the webpage
        nsSoup = BeautifulSoup(nsHTML, 'html.parser')
        # FInd each housing entry
        nsProperties = nsSoup.find_all('div', {'class', 'listing-item result js-listing-item'})

        for prop in nsProperties:
            image = prop.find('img')
            image = image['data-original']

            url = prop.find('a')
            url = "https://veniceprops.appfolio.com" + url['href']

            price = (prop.find('div', {'class':'sidebar__price rent-banner__text js-listing-blurb-rent'})).getText(strip=True)
            address = (prop.find('span', {'class':'u-pad-rm js-listing-address'})).getText()
            bedAndBath = (prop.find('span', {'class':'rent-banner__text js-listing-blurb-bed-bath'})).getText(strip=True)
            bedAndBath = bedAndBath.split()
            print(bedAndBath)
            bed = bedAndBath[0]

            bath = 0
            if len(bedAndBath) > 2:
                bath = bedAndBath[3]

            available = (prop.find('dd', {'class':'detail-box__value js-listing-available'}))
            if available:
                available = available.getText(strip=True)
            description = (prop.find('h2', {'class': 'listing-item__title js-listing-title'}))
            if description:
                description = description.getText(strip=True)
            else:
                description = ""
            
            print(address + " " + available)

            if available == "NOW":
                avail_date = datetime.datetime.now().date()
            else:
                avail_date = datetime.datetime.strptime(available, "%m/%d/%y").date()
            try:
                price = int(price[1:].replace(",", ""))
            except:
                price = -1

            d = {"image_url": image, "url": url, "price": int(price), "address": address, "num_bedrooms": bed, "num_bathrooms": bath, "description": description, "availability_date": avail_date, "active": True}
            print(d)
            callback(d)