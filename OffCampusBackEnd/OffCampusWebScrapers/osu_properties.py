from bs4 import BeautifulSoup
import requests
from OffCampusWebScrapers.scraper import Scraper
import datetime
import re

class OSUPropertiesScraper(Scraper):

    def __create_dictionaries(js):
        js = js[js.find("properties['"):js.find("// | Garages")]
        propList = []
        while "properties" in js:
            propDictionary = {}
            propDictionary['image'] = js[js.find("['")+2:js.find("']")] + "/main.jpg"
            prop = js[js.find("= ["):js.find(";")]
            js = OSUPropertiesScraper.__advance_one_property(js)

            propDictionary['beds'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = OSUPropertiesScraper.__advance_one_element(prop)
            propDictionary['address'] = prop[prop.find("'")+1:prop.find("&")].strip()
            propDictionary['utilities'] = prop[prop.find("&"):prop.find("',")].strip()
            prop = OSUPropertiesScraper.__advance_one_element(prop)
            propDictionary['city'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = OSUPropertiesScraper.__advance_one_element(prop)
            propDictionary['state'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = OSUPropertiesScraper.__advance_one_element(prop)
            propDictionary['zip_code'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = OSUPropertiesScraper.__advance_one_element(prop)
            propDictionary['price'] = prop[prop.find("$"):prop.find("/")].strip()
            propDictionary['amenities'] = prop[prop.find("/")+1:prop.find("',")].strip()
            prop = OSUPropertiesScraper.__advance_one_element(prop)
            propDictionary['other_info'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = OSUPropertiesScraper.__advance_one_element(prop)
            propDictionary['is_available'] = prop[prop.find("'")+1:prop.find("',")].strip()
            prop = OSUPropertiesScraper.__advance_one_element(prop)
            propDictionary['availability'] = prop[prop.find("'")+1:prop.find("',")].strip()

            propList.append(propDictionary)

        return propList

    def __advance_one_property(js):
        js = js[js.find(";")+1:]
        js = js.strip()
        while "/*" in js[:js.find(";")]:
            js = js[js.find(";")+1:]
            js = js.strip()
        return js[js.find(";")+1:]

    def __advance_one_element(prop):
        match = re.search("'\s*,", prop)
        string = match.group(0)
        return prop[prop.find(string)+1:]

    def __remove_tags(x):
        while "<" in x:
            x = x[:x.find("<")] + x[x.find(">")+1:]
        return x
    
    @classmethod
    def process_listings(cls, callback):
        reqURL = "https://www.osuproperties.com/properties/properties.js"
        baseURL = "https://www.osuproperties.com/propview.asp?cat="
        baseImage = "https://www.osuproperties.com/properties/"
        urlAddOns = ["onebed", "twobed", "threebed", "fourbed", "fivebed", "sixbed", "sevenbed"]

        js = (requests.get(url=reqURL)).text
        js = js[js.find("properties['"):js.find("// | Garages")]
        propList = OSUPropertiesScraper.__create_dictionaries(js)
        for prop in propList:
            image = prop['image'] + "/main.jpg"

            beds = urlAddOns.index(prop['beds']) + 1
            
            address = prop['address'] + ' ' + prop['city'] + ' ' + prop['state'] + ' ' + prop['zip_code']
            
            price = prop['price']
            if "-" in price:
                price = price[price.find("-")+1:]
            if "," in price:
                price = price[:price.find(",")] + price[price.find(",")+1:]
            while "$" in price:
                price = price[price.find("$")+1:]
            price = int(price)

            description = prop['other_info']
            description = OSUPropertiesScraper.__remove_tags(description)
            
            baths = (re.search('\d (bathroom|bath)', description, re.IGNORECASE))
            if baths != None:
                baths = baths.group()
                baths = baths[:baths.find(" ")]
                baths = float(baths)

            availability = prop['is_available']
            active = True if "yes" in availability else False

            if active:
                avail_date = prop['availability']
                avail_date = OSUPropertiesScraper.__remove_tags(avail_date)
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
        
            d = {"scraper": cls.__name__, "url": baseURL + urlAddOns[beds-1], "image": baseImage + image, "address": address, "beds": beds, "baths": baths, "description": description, "price": price, "availability_date": avail_date, "availability_mode": avail_mode, "active": True}
            print(d)
            callback(d)