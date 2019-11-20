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
            pc = requests.get(url=baseURL+str(pageNumber))
            pageNumber+=1
            html = request.text
            soup = BeautifulSoup(html, 'html.parser')
            properties = soup.find_all('div', {'class':'four columns views-column-1'})
            properties.extend(soup.find_all('div', {'class':'four columns views-column-2'}))
            properties.extend(soup.find_all('div', {'class':'four columns views-column-3'}))
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
                address =  address + "Columbus Ohio 43210"
                price = prop.find("div", {'class':'hover-details'}).findChildren("div", recursive=False)[1].getText()
                price = price[1:price.find(".")]
                bedrooms = prop.find("div", {'class':'field-item even'}).getText()
                bedrooms = bedrooms[:bedrooms.find(" ")]
                pageRequest = requests.get(url=link)
                listingHTML = pageRequest.text
                listingSoup = BeautifulSoup(listingHTML, 'html.parser')
                bath = listingSoup.find("div", {'class':'field field-name-field-baths field-type-taxonomy-term-reference field-label-hidden'})
                bath = bath.find("div", {'class':'field-item even'}).getText()
                bath = bath[0:bath.find(" ")]
                d = {"image_url": image, "url": url, "price": int(price), "address": address, "num_bedrooms": bedrooms, "num_bathrooms": bath, "description": None, "availability_date": datetime.datetime.now().date(), "active": True}
                print(d)
                callback(d)
            