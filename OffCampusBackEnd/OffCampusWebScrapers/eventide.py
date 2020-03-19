from bs4 import BeautifulSoup
import requests
import re
import base64
import json
from OffCampusWebScrapers.scraper import Scraper
import datetime


class EventideScraper(Scraper):
    def _remove_special_chars(string):
        chars = ['"', '$', ' ', '<br>', 'Bedrooms:', 'Bathrooms:', '\\']
        for char in chars:
            string = string.replace(char, '')
        return string
    
    @classmethod
    def process_listings(cls, callback):
        url = "https://unitavailability.rentmanager.com/Search_Result.aspx?command=Search_Result.aspx&template=eventideRentals&Page=1&start=0&mode=javascript&maxperpage=1000000&headerfooter=False&corpid=eventide&locations=default"
        req = requests.get(url=url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        listings = soup.find_all('tr')
        base_link_to_listing = "osurent.com"
        for item in listings:
            query_params = (item.find('a')['href'].replace(
                '"', '')).replace('\\', '')
            link_to_listing = "osurent.com" + query_params

            img = item.find('img')
            image_link = (img['src'].replace('"', '')).replace('\\', '')
            if img and img.has_attr('image&unitid'):
                image_link = image_link + " main image&unitId=" + img['image&unitid']
                image_link = image_link.replace('\\', '')
                image_link = image_link.replace('"', '')

            address_object = item.find('div', {'class': '\\\"address\\\"'})
            address = address_object.text

            availability = address_object.find('div').text
            availability = datetime.datetime.strptime(availability, '%B %d, %Y')

            price = item.find('div', {'class': '\\\"price\\\"'}).text
            price = EventideScraper._remove_special_chars(price)
            price = price.replace('.00', '')
            price = price.replace(',', '')

            address = item.find('div', {'class': '\\\"full-address\\\"'}).text
            address = address.replace('"', '')

            bed = item.find('div', {'class': '\\\"beds-baths\\\"'}).text
            bed = EventideScraper._remove_special_chars(bed)

            bath = item.find_all('div', {'class': '\\\"beds-baths\\\"'})[1].text
            bath = EventideScraper._remove_special_chars(bath)

            description_object = item.find(
                'div', {'class': '\\\"list-description\\\"'})
            description = description_object.find('p').text
            description = description.replace('"', '')

            d = {"image_url": image_link, "url": link_to_listing, "price": int(price), "address": address, "num_bedrooms": int(bed), "num_bathrooms": float(bath), "availability_date": availability, "availability_mode": 'Date', "active": True, "description": description}

            print(d)
            callback(d)
