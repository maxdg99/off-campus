from bs4 import BeautifulSoup
import requests
import base64
import json
from OffCampusWebScrapers.scraper import Scraper
import datetime

class PellaScraper(Scraper):

    def clean_date(date):
        date = date.replace('st', '')
        date = date.replace('nd', '')
        date = date.replace('rd', '')
        date = date.replace('th', '')
        date = date.replace(',', '')
        return date

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

                link = prop.find('a')['href']

                image = prop.find('img')["src"]

                address = prop.find('h2').getText()
                if address.find("St") >= 0:
                    address = address[:address.find("St")]
                if address.find("Ave") >= 0:
                    address = address[:address.find("Ave")]
                address = address + "Columbus Ohio 43210"

                for child in prop.find("div", {'class': 'hover-details'}).findChildren("div", recursive=False):
                    if "$" in child.text:
                        price = child.text[1:child.text.find(".")]

                bedrooms = prop.find("div", {'class': 'field-item even'}).getText()
                if "Efficiency" in bedrooms:
                    bedrooms = 1
                elif "House" in bedrooms:
                    bedrooms = 0 # What should we do with this?
                else:
                    bedrooms = bedrooms[:bedrooms.find(" ")]
                    bedrooms = bedrooms.replace('+', '')

                pageRequest = requests.get(url=link)
                listingHTML = pageRequest.text
                listingSoup = BeautifulSoup(listingHTML, 'html.parser')

                bath = listingSoup.find("div", {'class': 'field field-name-field-baths field-type-taxonomy-term-reference field-label-hidden'})
                bath = bath.find("div", {'class': 'field-item even'}).getText()
                bath = bath[0:bath.find(" ")]

                description = listingSoup.find("div", {'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
                if(description):
                    description = description.find("p").getText()
                else:
                    description = ""

                avail_date = listingSoup.find("span", {'class': 'available-date'})
                
                if avail_date:
                    avail_date = avail_date.getText()
                    avail_date = avail_date.split(' ')
                
                    if len(avail_date) >= 4:
                        avail_date = avail_date[1] + '/' + PellaScraper.clean_date(avail_date[2]) + '/' + avail_date[3]
                        avail_date = datetime.datetime.strptime(avail_date, "%B/%d/%Y").date()
                        avail_mode = "Date"
                        isAvailable = True
                    else:
                        avail_date = None
                        isAvailable = False
                        avail_mode = "None"
                else:
                    avail_date = None
                    avail_mode = "None"

                d = {"scraper": cls.__name__, "image_url": image, "url": link, "price": int(price), "address": address, "num_bedrooms": bedrooms, "num_bathrooms": bath, "description": description, "availability_date": avail_date, "availability_mode": avail_mode, "active": isAvailable}
                print(d)
                callback(d)
            