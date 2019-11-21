# Imports
from bs4 import BeautifulSoup
import requests
from OffCampusWebScrapers.scraper import Scraper
import datetime
from urllib.parse import urljoin

class AppfolioScraper():

    # URL of all properties
    #url = "https://ht.appfolio.com/listings"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Parses listings from page
    def process_listings(appfolioURL, callback):
        # Retrieves all information for webpage
        ns = requests.get(url=appfolioURL, headers=AppfolioScraper.headers)
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
            url = urljoin(appfolioURL, url['href'])

            price = (prop.find('div', {'class':'sidebar__price rent-banner__text js-listing-blurb-rent'})).getText(strip=True)
            address = (prop.find('span', {'class':'u-pad-rm js-listing-address'})).getText()
            bb = prop.find('span', {'class':'rent-banner__text js-listing-blurb-bed-bath'})
            if bb is None:
                continue
            bedAndBath = bb.getText(strip=True)
            bedAndBath = bedAndBath.split()
            print(bedAndBath)
            bed = 0
            if len(bedAndBath) > 2 and bedAndBath[1] == "bd":
                bed = bedAndBath[0]

            bath = 0
            if len(bedAndBath) > 4 and bedAndBath[4] == "ba":
                bath = bedAndBath[3]

            available = (prop.find('dd', {'class':'detail-box__value js-listing-available'}))
            if available:
                available = available.getText(strip=True)
            description = (prop.find('h2', {'class': 'listing-item__title js-listing-title'}))
            if description:
                description = description.getText(strip=True)
            else:
                description = ""
            
            print(address + " " + str(available))

            if available == "NOW":
                avail_date = datetime.datetime.now().date()
            elif available:
                avail_date = datetime.datetime.strptime(available, "%m/%d/%y").date()
            else:
                avail_date = None
            try:
                price = int(price[1:].replace(",", ""))
            except:
                price = -1

            d = {"image_url": image, "url": url, "price": int(price), "address": address, "num_bedrooms": bed, "num_bathrooms": bath, "availability_date": avail_date, "availability_mode": 'Date', "listed": True, "description": description}
            print(d)
            callback(d)


class HometeamAppfolioScraper(Scraper):
    url = "https://ht.appfolio.com/listings"
    
    def process_listings(callback):
        AppfolioScraper.process_listings(HometeamAppfolioScraper.url, callback)

class NorthsteppeScraper(Scraper):
    url = "https://northsteppe.appfolio.com/listings?1572716642290&filters%5Bproperty_list%5D=All%20OSU%20Campus%20Area%20Properties&theme_color=%23194261&filters%5Border_by%5D=date_posted"
    
    def process_listings(callback):
        AppfolioScraper.process_listings(NorthsteppeScraper.url, callback)

class VeniceScraper(Scraper):
    url = "https://veniceprops.appfolio.com/listings/listings"

    def process_listings(callback):
        AppfolioScraper.process_listings(VeniceScraper.url, callback)


class BuckeyeScraper(Scraper):
    url = "https://buckeye.appfolio.com/listings"

    def process_listings(callback):
        AppfolioScraper.process_listings(BuckeyeScraper.url, callback)