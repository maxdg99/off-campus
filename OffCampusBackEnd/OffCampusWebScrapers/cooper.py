from bs4 import BeautifulSoup
import requests
import re
import json
import datetime


class CooperScraper(Scraper):
    @classmethod
    def process_listings(cls, callback):
        base_url = "https://cooper-properties.com/properties/?fwp_availability=0&fwp_paged="
        url = base_url + "1"
        req = requests.get(url=url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        while soup.find_all('div', {'class': 'col-lg-4 col-md-6 featured-properties__property-wrap'}):
            listings = soup.find_all(
                'div', {'class': 'col-lg-4 col-md-6 featured-properties__property-wrap'})
            for listing in listings:
                link = listing.find(
                    'a', {'class': 'featured-properties__property'})['href']

                image_object = listing.find(
                    'div', {'class': 'featured-properties__image bg-cover'})
                immage_style = image_object['style']
                image_style = image_style[image_style.index("'"):]
                image_link = image_style[:image_style.index("'")-1]

                availability = listing.find(
                    'div', {'class': 'property-variants__status'}).text
                if availability:
                    availability = availability[availability.index('Available For '):]
                    availability = availability.splice(' ')
                    availability_year = int(availability[1])
                    if availability[0].lower() == "winter":
                        availability = datetime.datetime(availability_year, 12, 1)
                    if availability[0].lower() == "spring":
                        availability = datetime.datetime(availability_year, 3, 1)
                    if availability[0].lower() == "summer":
                        availability = datetime.datetime(availability_year, 6, 1)
                    if availability[0].lower() == "fall":
                        availability = datetime.datetime(availability_year, 9, 1)
                    avail_mode = 'Month'
                else:
                    avil_mode = 'None'

                address = listing.find(
                    'h4', {'class': 'featured-properties__title'}).text

                req = requests.get(url=link)
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')

                # d = {"image_url": image_link, "url": link_to_listing, "price": int(price), "address": address, "num_bedrooms": int(bed), "num_bathrooms": float(bath), "availability_date": availavility, "availability_mode": 'Date', "listed": True, "description": description}
                # print(d)
