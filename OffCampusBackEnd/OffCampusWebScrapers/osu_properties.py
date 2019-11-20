from bs4 import BeautifulSoup
import requests
import base64
import json
from OffCampusWebScrapers.scraper import Scraper
import datetime
import re

class PellaScraper(Scraper):
    
    def process_listings(callback):
        reqURL = "https://www.osuproperties.com/properties/properties.js"
        baseURL = "https://www.osuproperties.com/propview.asp?cat="
        baseImage = "https://www.osuproperties.com/properties/"
        urlAddOns = ["onebed", "twobed", "threebed", "fourbed", "fivebed", "sixbed", "sevenbed"]
        js = (requests.get(url=reqURL)).text
        js = js[js.find("properties['"):js.find("// | Garages")]
        properties = []
        while "properties" in js:
            image = js[js.find("[']")+1:js.find("']")] + "main.jpg"
            propJS = js[js.find("= ["):js.find(";")]
            js = js[js.find(";")+1:]
            beds = propJS[propJS.find("'")+1:propJS.find("',")]
            i = 1
            for x in urlAddOns:
                if x == beds:
                    beds = 1
                i += 1
            propJS = propJS[propJS.find("',")+1:]
            address = propJS[propJS.find("'")+1:propJS.find('&')]
            propJS = propJS[propJS.find("',")+1:]
            address += " " + propJS[propJS.find("'")+1:propJS.find("',")]
            propJS = propJS[propJS.find("',")+1:]
            address += " " + propJS[propJS.find("'")+1:propJS.find("',")]
            propJS = propJS[propJS.find("',")+1:]
            address += " " + propJS[propJS.find("'")+1:propJS.find("',")]
            propJS = propJS[propJS.find("',")+1:]
            price = propJS[propJS.find("$")+1:propJS.find("/")]
            if "," in price:
                price = price[:price.find(",")] + price[price.find(",")+1:]
            propJS = propJS[propJS.find("',")+1:]
            description = propJS[propJS.find("'")+1:propJS.find("',")]
            while "<" in description:
                description = description[:description.find("<")] + description[description.find(">")+1:]
            bathroom = (re.search('\d( \d\/\d)? bathroom', description, re.IGNORECASE))
            if bathroom != None:
                bathroom = bathroom.group()
                bathroom = bathroom[:bathroom.find(" ")]
            propJS = propJS[propJS.find("',")+1:]
            propJS = propJS[propJS.find("',")+1:]
            availability = propJS[propJS.find("'")+1:propJS.find("',")]
            d = {"image_url": baseImage + image, "url": baseURL + urlAddOns[int(beds)-1], "price": int(price), "address": address, "num_bedrooms": int(beds), "num_bathrooms": int(bathroom), "description": description, "availability_date": availability, "active": True}
            print(d)
            callback(d)
