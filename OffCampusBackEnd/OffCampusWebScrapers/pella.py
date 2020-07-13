from bs4 import BeautifulSoup
import re
import requests
from OffCampusWebScrapers.scraper import Scraper
import datetime

class PellaScraper(Scraper):

    def __clean_date(date):
        date = date.replace('st', '')
        date = date.replace('nd', '')
        date = date.replace('rd', '')
        date = date.replace('th', '')
        date = date.replace(',', '')
        return date

    def __clean_month(month):
        month = re.sub("Sept$", "September", month)
        return month

    @classmethod
    def process_listings(cls, callback):
        baseURL = "http://pellaco.com/property-search?term_node_tid_depth=All&field_bedrooms_tid=All&page="
        pageNumber = 0  
        isNextPage = True
        while isNextPage:
            firstTime = False
            request = requests.get(url=baseURL+str(pageNumber))
            pageNumber += 1

            html = request.text
            soup = BeautifulSoup(html, 'html.parser')

            properties = soup.find_all(
                'div', {'class': 'four columns views-column-1'})
            properties.extend(soup.find_all(
                'div', {'class': 'four columns views-column-2'}))
            properties.extend(soup.find_all(
                'div', {'class': 'four columns views-column-3'}))
            if len(properties) == 0:
                isNextPage = False

            for prop in properties:

                url = prop.find('a')['href']

                image = prop.find('img')["src"]

                for child in prop.find("div", {'class': 'hover-details'}).findChildren("div", recursive=False):
                    if "$" in child.text:
                        price = child.text[1:child.text.find(".")]
                        price = int(price)

                beds = prop.find("div", {'class': 'field-item even'}).getText()
                if "Efficiency" in beds:
                    beds = 1
                elif "House" in beds:
                    beds = None # What should we do with this?
                elif "Commercial" in beds:
                    beds = None
                else:
                    beds = beds[:beds.find(" ")]
                    beds = beds.replace('+', '')
                    beds = int(beds)

                listing_req = requests.get(url=url)
                listing_html = listing_req.text
                listing_soup = BeautifulSoup(listing_html, 'html.parser')

                address = listing_soup.find('h2').getText()
                title = listing_soup.find('h1').getText()
                unit_re = re.findall("#\d|Apt [A-Z]", title)
                unit = ""
                if len(unit_re) > 0:
                    unit = unit_re[0]
                    address = address.replace(unit, '')
                    unit = unit.strip()
                address = address.strip()

                baths = listing_soup.find("div", {'class': 'field field-name-field-baths field-type-taxonomy-term-reference field-label-hidden'})
                baths = baths.find("div", {'class': 'field-item even'}).getText()
                baths = baths[0:baths.find(" ")]
                float(baths)

                description = listing_soup.find("div", {'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
                if(description):
                    description = description.find("p").getText()
                else:
                    description = ""

                avail_date = listing_soup.find("span", {'class': 'available-date'})
                
                if avail_date:
                    avail_date = avail_date.getText()
                    avail_date = avail_date.split(' ')
                    if '' in avail_date:
                        avail_date.remove('')
                    print(avail_date)
                    if len(avail_date) == 4:
                        print(avail_date)
                        avail_date = PellaScraper.__clean_month(avail_date[1]) + '/' + PellaScraper.__clean_date(avail_date[2]) + '/' + avail_date[3]
                        avail_date = datetime.datetime.strptime(avail_date, "%B/%d/%Y").date()
                        avail_mode = "Date"
                        is_avail = True
                    elif len(avail_date) == 3: 
                        avail_date = PellaScraper.__clean_month(avail_date[1]) + '/1/' + avail_date[2]
                        avail_date = datetime.datetime.strptime(avail_date, "%B/%d/%Y").date()
                        avail_mode = "Month"
                        is_avail = True
                    else:
                        avail_date = None
                        is_avail = False
                        avail_mode = "None"
                else:
                    avail_date = None
                    avail_mode = "None"
                    is_avail = False

                d = {"scraper": cls.__name__, "url": url, "image": image, "address": address, "beds": beds, "baths": baths, "description": description, "price": price, "availability_date": avail_date, "availability_mode": avail_mode, "active": is_avail, "unit": unit}
                print(d)
                #callback(d)
            