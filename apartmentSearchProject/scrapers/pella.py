from bs4 import BeautifulSoup
import requests
import base64
import json

class PellaScraper(Scraper):
    baseURL = "http://pellaco.com/property-search?term_node_tid_depth=All&field_bedrooms_tid=All&page="
    
    def process_listings(callback):
        pageNumber = 0  
        isNextPage = True
        pcProperties = []
        numProp = 0
        while isNextPage:
            firstTime = False
            pc = requests.get(url=baseURL+str(pageNumber))
            pageNumber+=1
            pcHTML = pc.text
            pcSoup = BeautifulSoup(pcHTML, 'html.parser')
            pcProperties = pcSoup.find_all('div', {'class':'four columns views-column-1'})
            pcProperties.extend(pcSoup.find_all('div', {'class':'four columns views-column-2'}))
            pcProperties.extend(pcSoup.find_all('div', {'class':'four columns views-column-3'}))
            if len(pcProperties) == 0:
                isNextPage = False
            for prop in pcProperties:
                numProp += 1
                link = prop.find('a')['href']
                image = prop.find('img')["src"]
                address = prop.find('h2').getText()
                if address.find("-") >= 0:
                    address = address[address.find("-"):]
                address =  address + "Columbus Ohio 43210"
                price = prop.find("div", {'class':'hover-details'}).findChildren("div", recursive=False)[1].getText();
                bedrooms = prop.find("div", {'class':'field-item even'}).getText()
                pageRequest = requests.get(url=link)
                listingHTML = pageRequest.text
                listingSoup = BeautifulSoup(listingHTML, 'html.parser')
                bath = listingSoup.find("div", {'class':'field field-name-field-baths field-type-taxonomy-term-reference field-label-hidden'})
                bath = bath.find("div", {'class':'field-item even'}).getText()
                bath = bath[0:bath.find(" ")]
            