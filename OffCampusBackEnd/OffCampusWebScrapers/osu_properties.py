from bs4 import BeautifulSoup
import requests
import base64
import json
from OffCampusWebScrapers.scraper import Scraper
import datetime
import re

class PellaScraper(Scraper):

    def _create_dictionaries(js):
        js = js[js.find("properties['"):js.find("// | Garages")]
        propList = []
        while "properties" in js:
            propDictionary = {}
            propDictionary['image'] = js[js.find("['")+2:js.find("']")] + "/main.jpg"
            prop = js[js.find("= ["):js.find(";")]
            js = _advance_one_property(js)

            propDictionary['beds'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = _advance_one_element(prop)
            propDictionary['address'] = prop[prop.find("'")+1:prop.find("&")].strip()
            propDictionary['utilities'] = prop[prop.find("&"):prop.find("',")].strip()
            prop = _advance_one_element(prop)
            propDictionary['city'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = _advance_one_element(prop)
            propDictionary['state'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = _advance_one_element(prop)
            propDictionary['zip_code'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = _advance_one_element(prop)
            propDictionary['price'] = prop[prop.find("$"):prop.find("/")].strip()
            propDictionary['amenities'] = prop[prop.find("/")+1:prop.find("',")].strip()
            prop = _advance_one_element(prop)
            propDictionary['other_info'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = _advance_one_element(prop)
            propDictionary['is_available'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = _advance_one_element(prop)
            propDictionary['availability'] = prop[prop.find("'")+1:prop.find("',")].strip()

            propList.append(propDictionary)

        return propList

    def _advance_one_property(js):
        js = js[js.find(";")+1:]
        js = js.strip()
        while "/*" in js[:js.find(";")]:
            js = js[js.find(";")+1:]
            js = js.strip()
        return js[js.find(";")+1:]

    def _advance_one_element(prop):
        match = re.search("'\s*,", prop)
        string = match.group(0)
        return prop[prop.find(string)+1:]

    def _remove_tags(x):
        while "<" in x:
            x = x[:x.find("<")] + x[x.find(">")+1:]
        return x

    def process_listings(callback):
        reqURL = "https://www.osuproperties.com/properties/properties.js"
        baseURL = "https://www.osuproperties.com/propview.asp?cat="
        baseImage = "https://www.osuproperties.com/properties/"
        urlAddOns = ["onebed", "twobed", "threebed", "fourbed", "fivebed", "sixbed", "sevenbed"]

        js = (requests.get(url=reqURL)).text
        js = js[js.find("properties['"):js.find("// | Garages")]
        propList = _create_dictionaries(js)
        for prop in propList:
            image = prop['image'] + "/main.jpg"

            i = 1
            for x in urlAddOns:
                if x == prop['beds']:
                    beds = i
                i += 1
            
            address = prop['address'] + ' ' + prop['city'] + ' ' + prop['state'] + ' ' + prop['zip_code']
            
            price = prop['price']
            if "-" in price:
                price = price[price.find("-")+1:]
            if "," in price:
                price = price[:price.find(",")] + price[price.find(",")+1:]
            while "$" in price:
                price = price[price.find("$")+1:]

            description = prop['other_info']
            description = _remove_tags(description)
            
            bathroom = (re.search('\d( \d\/\d)? bathroom', description, re.IGNORECASE))
            if bathroom != None:
                bathroom = bathroom.group()
                bathroom = bathroom[:bathroom.find(" ")]
                bathroom = int(bathroom)

            availability = prop['is_available']
            listed = True if "yes" in availability else False

            if listed:
                avail_date = prop['availability']
                avail_date = _remove_tags(avail_date)
                if "now" in avail_date.lower():
                    avail_mode = "Now"
                    avail_date = None
                elif "school year" in avail_date.lower():
                    avail_date = avail_date[avail_date.find(" ")+1:]
                    avail_date = avail_date[:avail_date.find(" ")]
                    avail_date = avail_date[:avail_date.find("-")]
                    avail_date = avail_date.strip()
                    avail_date = "8/1/" + avail_date
                    avail_date = datetime.datetime.strptime(avail_date, "%m/%d/%Y").date()
                    avail_mode = "Season"
                else:
                    match = re.search('\w+ \d+, \d+', avail_date)
                    avail_date = datetime.datetime.strptime(match[0], "%B %d, %Y").date()
                    avail_mode = "Date"
        
            d = {"image_url": baseImage + image, "url": baseURL + urlAddOns[int(beds)-1], "price": int(price), "address": address, "num_bedrooms": int(beds), "num_bathrooms": bathroom, "availability_date": avail_date, "availability_mode": avail_mode, "listed": listed, "description": description}
            print(d)
            callback(d)