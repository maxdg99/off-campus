from bs4 import BeautifulSoup
import requests
import re
from OffCampusWebScrapers.scraper import Scraper
import datetime


class PeakScraper(Scraper):
    @classmethod
    def process_listings(cls, callback):
        req_url = "https://peakpropertygroup.com/rental-search/?region=columbus"
        req = requests.get(url=req_url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        table_entries = soup.find_all('tr', {'class': 'property'})
        for entry in table_entries:
            if entry["data-region"] == "Columbus":
                url = entry['data-permalink']
                image = entry.find('img')['src']
                address = entry['data-title']
                units = entry.find('table', {'class': 'units'})
                if units != None:
                    units = units.find('tbody').find_all('tr')
                    for u in units:
                        number_unit = u.find('td', {'class': 'unit'}).text
                        unit = ""
                        street_number = number_unit
    
                        if ' ' in number_unit:
                            number_unit = number_unit.split()
                            street_number = number_unit[0]
                            unit = number_unit[1]
                        elif re.search('[a-zA-Z]+', number_unit):
                            unit = re.search('[a-zA-Z]+', number_unit).group(0)
                            street_number = number_unit.replace(unit, '')

                        range_street_number = re.search('^\d+-?\d* ', address)
                        single_address = address.replace(range_street_number[0], '')
                        single_address = f'{street_number} {single_address}'
                        print(single_address)

                        price = u.find('td', {'class': 'rent'}).text
                        price = price.replace('$', '')
                        price = price.replace(',', '')
                        price = price[:-3]
                        int(price)

                        bed_bath = u.find('td', {'class': 'type'}).text
                        bed_bath_re = re.findall('\d+', bed_bath)
                        if len(bed_bath_re) > 0:
                            if 'Studio' in bed_bath:
                                beds = 1
                                baths = bed_bath_re[0]
                            else:
                                beds = bed_bath_re[0]
                                baths = bed_bath_re[1]
                            int(beds)
                            float(baths)
                        else:
                            beds = None
                            baths = None

                        availability = u.find('td', {'class': 'available'})
                        availability = availability.text
                        if availability == "Now":
                            avail_date = None
                            avail_mode = 'Now'
                            isAvailable = True
                        elif availability:
                            avail_date = datetime.datetime.strptime(
                                availability, "%m/%d/%y").date()
                            avail_mode = 'Date'
                            isAvailable = True
                        else:
                            avail_date = None
                            avail_mode = 'None'
                            isAvailable = False

                        d = {"scraper": cls.__name__, "url": url, "image": image, "address": single_address, "beds": beds, "baths": baths,
                            "price": price, "availability_date": avail_date, "availability_mode": avail_mode, "active": True, "unit": unit}
                        print(d)
                        callback(d)
