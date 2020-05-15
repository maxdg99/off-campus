from bs4 import BeautifulSoup
import datetime
import json
from OffCampusWebScrapers.scraper import Scraper
import requests
import re
from urllib.parse import urljoin

# WIP

class EventideScraper(Scraper):

    @staticmethod
    def _remove_special_chars(string):
        chars = ['"', '$', ' ', '<br>', 'Bedrooms:', 'Bathrooms:', '\\']
        for char in chars:
            string = string.replace(char, '')
        return string
    
    @classmethod
    def process_listings(cls, callback):
        scrape_url = "https://unitavailability.rentmanager.com/Search_Result.aspx?command=Search_Result.aspx&template=eventideRentals&Page=1&start=0&mode=javascript&maxperpage=1000000&headerfooter=False&corpid=eventide&locations=default"
        req = requests.get(url=scrape_url, headers={"User-Agent": "Mozilla/5.0"})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        listings = soup.find_all('tr')
        for listing in listings:
            query_params = (listing.find('a')['href'].replace('"', '')).replace('\\', '')
            url = urljoin("osurent.com", query_params)

            image_object = listing.find('img')
            image = (image_object['src'].replace('"', '')).replace('\\', '')
            if image_object and image_object.has_attr('image&unitid'):
                image = image + " main image&unitId=" + image_object['image&unitid']
                image = image.replace('\\', '')
                image = image.replace('"', '')

            address = listing.find('div', {'class': '\\\"full-address\\\"'}).text
            address = address.replace('"', '')

            availability_date = listing.find('div', {'class': '\\\"availability\\\"'}).getText(strip=True)
            availability_date = datetime.datetime.strptime(availability_date, '%B %d, %Y')

            price = listing.find('div', {'class': '\\\"price\\\"'}).text
            price = EventideScraper._remove_special_chars(price)
            price = price.replace('.00', '')
            price = price.replace(',', '')
            price = int(price)

            beds = listing.find('div', {'class': '\\\"beds-baths\\\"'}).text
            beds = EventideScraper._remove_special_chars(beds)
            beds = int(beds)

            baths = listing.find_all('div', {'class': '\\\"beds-baths\\\"'})[1].text
            baths = EventideScraper._remove_special_chars(baths)
            baths = float(baths)

            description_object = listing.find(
                'div', {'class': '\\\"list-description\\\"'})
            description = description_object.find('p').text
            description = description.replace('"', '')

            d = {'scraper': cls.__name__, 'url': url, 'image': image, 'address': address, 'beds': beds, 'baths': baths, 'description': description, 'price': price, 'availability_date': availability_date, 'availability_mode': 'Date', 'active': True}
            print(d)
            callback(d)
