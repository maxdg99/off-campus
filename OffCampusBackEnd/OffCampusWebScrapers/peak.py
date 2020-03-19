from bs4 import BeautifulSoup
import requests
import re
import base64
import json
from OffCampusWebScrapers.scraper import Scraper
import datetime

class PeakScraper(Scraper):
    @classmethod
    def process_listings(cls, callback):
        url = "https://peakpropertygroup.com/rental-search/?region=columbus"
        req = requests.get(url=url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        table_entries = soup.find_all('tr', {'class': 'property'})
        for entry in table_entries:
            link = entry['data-permalink']
            image_url = entry.find('img')['src']
            address = entry['data-title']
            units = entry.find('table', {'class': 'units'})
            if units != None:
                units = units.find('tbody').find_all('tr')
                for u in units:
                    unit = u.find('td', {'class': 'unit'}).text

                    price = u.find('td', {'class': 'rent'}).text
                    price = price.replace('$', '')
                    price = price.replace(',', '')
                    price = price[:-3]

                    bed_bath = u.find('td', {'class': 'type'}).text
                    bed_bath_re = re.findall('\d+', bed_bath)
                    if 'Studio' in bed_bath:
                        bed = 1
                        bath = bed_bath_re[0]
                    else:
                        bed = bed_bath_re[0]
                        bath = bed_bath_re[1]

                    availability = u.find('td', {'class': 'available'})
                    availability = availability.text
                    if availability == "Now":
                        avail_date = None
                        avail_mode = 'Now'
                        isAvailable = True
                    elif availability:
                        avail_date = datetime.datetime.strptime(availability, "%m/%d/%y").date()
                        avail_mode = 'Date'
                        isAvailable = True
                    else:
                        avail_date = None
                        avail_mode = 'None'
                        isAvailable = False


                    d = {"scraper": cls.__name__, "image_url": image_url, "url": link, "price": int(price), "address": address, "num_bedrooms": int(bed), "num_bathrooms": int(bath), "availability_date": avail_date, "availability_mode": avail_mode, "active": isAvailable, "description": "", "unit": unit}
                    print(d)
                    callback(d)
                