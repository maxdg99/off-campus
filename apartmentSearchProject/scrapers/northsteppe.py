from bs4 import BeautifulSoup
import requests
import base64
import json
from scrapers.scraper import Scraper
import datetime

class NorthsteppeScraper(Scraper):

    northsteppeURL = "https://northsteppe.appfolio.com/listings?1572716642290&filters%5Bproperty_list%5D=All%20OSU%20Campus%20Area%20Properties&theme_color=%23194261&filters%5Border_by%5D=date_posted"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }


    def process_listings(callback):
        ns = requests.get(url=NorthsteppeScraper.northsteppeURL, headers=NorthsteppeScraper.headers)
        nsHTML = ns.text
        nsSoup = BeautifulSoup(nsHTML, 'html.parser')
        nsProperties = nsSoup.find_all('div', {'class', 'listing-item result js-listing-item'})
        for prop in nsProperties:
            image = prop.find('img')
            image = image['data-original']
            url = prop.find('a')
            url = "https://northsteppe.appfolio.com" + url['href']
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
