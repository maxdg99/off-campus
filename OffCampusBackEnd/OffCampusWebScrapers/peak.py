from bs4 import BeautifulSoup
import requests
import re
import base64
import json
from OffCampusWebScrapers.scraper import Scraper
import datetime

class PeakScraper(Scraper):
    url = "https://peakpropertygroup.com/rental-search/?region=columbus"
    def process_listings(callback):
        req = requests.get(url=url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        table_entires = soup.find_all('td', {'class': 'property'})
        for entry in table_entries:
            image_url = entry.find('img')['src']
            units_table = entry.find('table', {'class': 'centered'})
            address = entry['data-title']
            units = units_table.find('tr')
            for unit in units:
                link = entry['data-link']
                unit = entry.find('td', {'class': 'unit'})
                unit_re = re.findall('\d+|[A-Z]\d*|\d[A-Z]|1/2')

                bed_bath = entry.find('td', {'class': 'type'})
                bed_bath_re = re.findall('\d+', bed_bath)
                bed = bed_bath_re[0]
                bath = bed_bath_re[1]

                availability = entry.find('td', {'class': 'available'})
                if available == "Now":
                    avail_date = None
                    avail_mode = 'Now'
                elif available:
                    avail_date = datetime.datetime.strptime(available, "%m/%d/%y").date()
                    avail_mode = 'Date'
                else:
                    avail_date = None
                    avail_mode = 'None'

                d = {"image_url": image, "url": link, "price": int(price), "address": address, "num_bedrooms": int(bedrooms), "num_bathrooms": int(bath), "availability_date": avail_date, "availability_mode": avail_mode, "listed": isAvailable, "description": None}
                print(d)
                callback(d)
            