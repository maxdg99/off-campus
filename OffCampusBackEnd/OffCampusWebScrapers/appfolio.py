# Imports
from bs4 import BeautifulSoup
import datetime
from OffCampusWebScrapers.scraper import Scraper
import requests
import re
from urllib.parse import urljoin
from OffCampusBackEnd.utility import format_address

class AppfolioScraper():

    def process_listings(appfolioURL, className, callback):
        # Retrieves all information for webpage
        req = requests.get(url=appfolioURL, headers={"User-Agent": "Mozilla/5.0"})
        # Pulls out just the HTML Template
        html = req.text
        # Create an HTML Scraper for the webpage
        soup = BeautifulSoup(html, 'html.parser')
        # FInd each housing entry
        properties = soup.find_all('div', {'class', 'listing-item result js-listing-item'})

        for prop in properties:
            image = prop.find('img')['data-original']

            url = urljoin(appfolioURL, prop.find('a')['href'])

            price = (prop.find('div', {'class':'sidebar__price rent-banner__text js-listing-blurb-rent'})).getText(strip=True)

            address = (prop.find('span', {'class':'u-pad-rm js-listing-address'})).getText(strip=True)

            bed_and_bath = prop.find('span', {'class':'rent-banner__text js-listing-blurb-bed-bath'})
            if bed_and_bath is None:
                continue
            bed_and_bath = bed_and_bath.getText(strip=True).split()

            beds = 0
            if len(bed_and_bath) > 2 and bed_and_bath[1] == "bd":
                beds = bed_and_bath[0]
                int(beds)

            baths = 0
            if len(bed_and_bath) > 4 and bed_and_bath[4] == "ba":
                baths = bed_and_bath[3]
                baths = float(baths)

            availability = prop.find('dd', {'class':'detail-box__value js-listing-available'})
            if availability:
                availability = availability.getText(strip=True)
                if availability == "NOW":
                    availability_date = None
                    availability_mode = "Now"
                else:
                    availability_date = datetime.datetime.strptime(availability, "%m/%d/%y")
                    availability_mode = "Date"
            else:
                availability_date = None
                availability_mode = "None"

            try:
                price = int(price[1:].replace(",", ""))
            except:
                price = None

            description = (prop.find('h2', {'class': 'listing-item__title js-listing-title'}))
            if description:
                description = description.getText(strip=True)
            else:
                description = ""

            #address = format_address(address)

            d = {"scraper": className, "url": url, "image": image, "address": address, "beds": beds, "baths": baths, "description": description, "price": price, "availability_date": availability_date, "availability_mode": availability_mode, "active": True}
            print(d)
            callback(d)


class NorthsteppeScraper(Scraper):
    url = "https://northsteppe.appfolio.com/listings?1572716642290&filters%5Bproperty_list%5D=All%20OSU%20Campus%20Area%20Properties&theme_color=%23194261&filters%5Border_by%5D=date_posted"
    
    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(NorthsteppeScraper.url, cls.__name__, callback)

class VeniceScraper(Scraper):
    url = "https://veniceprops.appfolio.com/listings/listings"

    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(VeniceScraper.url, cls.__name__, callback)


class BuckeyeScraper(Scraper):
    url = "https://buckeye.appfolio.com/listings"

    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(BuckeyeScraper.url, cls.__name__, callback)