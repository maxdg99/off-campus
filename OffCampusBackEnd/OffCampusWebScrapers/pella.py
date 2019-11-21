from bs4 import BeautifulSoup
import requests
import base64
import json
from OffCampusWebScrapers.scraper import Scraper
import datetime

class PellaScraper(Scraper):
    baseURL = "http://pellaco.com/property-search?term_node_tid_depth=All&field_bedrooms_tid=All&page="
    def process_listings(callback):
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
                if address.find("-") >= 0:
                    address = address[address.find("-"):]
                address = address + "Columbus Ohio 43210"

                price = prop.find("div", {'class': 'hover-details'}).findChildren("div", recursive=False)[1].getText()
                price = price[1:price.find(".")]

                bedrooms = prop.find("div", {'class': 'field-item even'}).getText()
                if "Efficiency" in bedrooms:
                    bedrooms = 1
                else:
                    bedrooms = bedrooms[:bedrooms.find(" ")]

                pageRequest = requests.get(url=link)
                listingHTML = pageRequest.text
                listingSoup = BeautifulSoup(listingHTML, 'html.parser')

                bath = listingSoup.find("div", {'class': 'field field-name-field-baths field-type-taxonomy-term-reference field-label-hidden'})
                bath = bath.find("div", {'class': 'field-item even'}).getText()
                bath = bath[0:bath.find(" ")]

                description = listingSoup.find("div", {'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
                description = description.find("p").getText()

                avail_date = listingSoup.find("span", {'class': 'available-date'}).getText()
                avail_date = avail_date.split(' ')
                if "Not" in avail_date[0]:
                    avail_date = None
                    isAvailable = False
                    avail_mode = "None"
                else:
                    avail_date = avail_date[1] + '/01/' + avail_date[2]
                    avail_date = datetime.datetime.strptime(avail_date, "%B/%d/%Y").date()
                    avail_mode = "Month"
                    isAvailable = True
                d = {"image_url": image, "url": link, "price": int(price), "address": address, "num_bedrooms": int(bedrooms), "num_bathrooms": int(bath), "availability_date": avail_date, "availability_mode": avail_mode, "listed": isAvailable, "description": description}
                print(d)
                callback(d)
            