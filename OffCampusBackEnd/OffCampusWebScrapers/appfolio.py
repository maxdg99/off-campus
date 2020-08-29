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

            address = (prop.find('span', {'class':'u-pad-rm js-listing-address'})).getText()

            if ' - ' in address and className == 'VeniceScraper':
                two_part_address = address.index(' - ')
                address = address[two_part_address:]

            number_letter = re.findall(' \d{1,3}[ ]?[A-Za-z],', address)
            letter_number = re.findall(' [A-Za-z]\d', address)
            letter = re.findall('[# ][A-Za-z][, ]', address)
            number = re.findall('[# ]\d{1,3},', address)
            unit = ""

            if len(number_letter) > 0:
                unit = number_letter[0]
                address = address.replace(unit, ',')
                unit = unit.replace(' ', '').replace(',', '')
            elif len(letter_number) > 0:
                unit = letter_number[0]
                address = address.replace(unit, ',')
                unit = unit.replace(' ', '').replace(',', '')
            elif len(letter) > 0:
                print(letter)
                if len(letter) >= 2:
                    unit = letter[1]
                else:
                    unit = letter[0]
                address = address.replace('  ', ' ')
                if ',' in unit:
                    address = address.replace(unit, ',')
                else:
                    address = address.replace(unit, ' ')
                unit = unit.replace(' ', '').replace(',', '')
            elif len(number) > 0:
                if len(number) >= 2:
                    unit = number[1]
                else:
                    unit = number[0]
                address = address.replace('  ', ' ')
                address = address.replace(unit, ',')
                unit = unit.replace(' ', '').replace(',', '').replace('#', '')

            address = address.replace('Apt.', '')
            address = address.replace('Apartment', '')
            address = address.replace('Unit', '')
            address = address.replace(',,', ',')
            address = address.replace(' , ', ', ')
            address = address.replace(' -,', ',')
            address = address.replace(' - ', '')

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

            d = {"scraper": className, "url": url, "image": image, "address": address, "beds": beds, "baths": baths, "description": description, "price": price, "availability_date": availability_date, "availability_mode": availability_mode, "active": True, "unit": unit}
            print(d)
            #callback(d)


class NorthsteppeScraper(Scraper):
    url = "https://northsteppe.appfolio.com/listings?1572716642290&filters%5Bproperty_list%5D=All%20OSU%20Campus%20Area%20Properties&theme_color=%23194261&filters%5Border_by%5D=date_posted"
    
    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(NorthsteppeScraper.url, cls.__name__, callback)

class VeniceScraper(Scraper):
    url = "https://veniceprops.appfolio.com/listings"

    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(VeniceScraper.url, cls.__name__, callback)

class BuckeyeScraper(Scraper):
    url = "https://buckeye.appfolio.com/listings"

    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(BuckeyeScraper.url, cls.__name__, callback)

class MyFirstPlaceScraper(Scraper): #bad
    url = "https://my1stplace.appfolio.com/listings"
    
    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(MyFirstPlaceScraper.url, cls.__name__, callback)
    
class LegacyScraper(Scraper):
    url = "https://legacymgmt.appfolio.com/listings"

    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(LegacyScraper.url, cls.__name__, callback)

class OSULiveScraper(Scraper):
    url = "https://osulive.appfolio.com/listings"

    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(OSULiveScraper.url, cls.__name__, callback)

class VIPScraper(Scraper):
    url = "https://viprealtyhomes.appfolio.com/listings"

    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(VIPScraper.url, cls.__name__, callback)