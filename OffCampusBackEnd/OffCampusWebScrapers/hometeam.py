from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin
from OffCampusWebScrapers.scraper import Scraper
from OffCampusWebScrapers.appfolio import AppfolioScraper

# This is not done.  Need to call appfolio scraper in hometeam scraper, fix compare address, and creat listings

class HometeamAppfolioScraper(Scraper):
    url = "https://ht.appfolio.com/listings"
    
    def process_listings(callback):
        AppfolioScraper.process_listings(HometeamAppfolioScraper.url, callback)

class HometeamScraper(Scraper):
    hometeamURL = "https://www.hometeamproperties.net/osu-off-campus-housing"
    htAppfolioListings = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def add_ht_appfolio_listings(data)
    {
        htAppfolioListings.append(data)
    }

    def dict_from_listing(listingDiv):
        data = {}
        data["image_url"] = listingDiv.find("img")["src"]
        data["url"] = urljoin(HometeamScraper.hometeamURL, listingDiv.find("a")["href"])
        address = listingDiv.find("h4").text
        address = address[0:address.find(":")].strip()
        data["address"] = address + ", Columbus, OH 43210"

        bedbath = listingDiv.find("strong").text.split()
        data["num_bedrooms"] = bedbath[0]
        data["num_bathrooms"] = bedbath[2]

        return data

    def process_listings(callback):
        HometeamAppfolioScraper.process_listings(add_ht_appfolio_listings)

        ht = requests.get(url=HometeamScraper.hometeamURL)
        htHTML = ht.text
        htSoup = BeautifulSoup(htHTML, 'html.parser')
        htProperties = htSoup.find("div", {"class": "grid"})
        htListings = []
        for listingDiv in htProperties.findAll("div", recursive=False):
            htListings.append(HometeamScraper.dict_from_listing(listingDiv))

        for ht in htListings:
            for af in htAppfolioListings:
                if compare_address(ht["address"], af["address"]):
                    listing = {"image_url": ht["image_url"], "url": ht["url"], "price": af["price"], "address": ht["address"], "num_bedrooms": ht["num_bedrooms"], "num_bathrooms": ht["num_bathrooms"], "availability_date": af["availability_date"], "availability_mode": 'Date', "listed": True, "description": ht["description"]}
                    print(listing)

    def get_address_components(address):
        direction = re.search('North|South|East|West|north|south|east|west|N|S|E|W', address)
        if direction != None:
            direction = direction[0]
            address = address.replace(direction, '')
            direction = direction.lower()
            if 'n' == direction:
                direction = 'north'
            if 'e' == direction:
                direction = 'east'
            if 's' == direction:
                direction = 'south'
            if 'w' == direction:
                direction = 'west'
            
        
        road = re.search('Avenue|Ave|Ave\.|Street|St|St\.|Road|Rd|Rd.', address, re.IGNORECASE)
        if road != None:
            road = road[0]
            address = address.replace(road, '')
        
        number_range = re.search('^\d+-\d+', address)
        numbers = re.findall('\d+[a-zA-Z]?', address)
        letters = re.findall(' [a-zA-Z] | [a-zA-Z],', address)
        upper_range = lower_range = zipcode = unit = None
        if number_range != None:
            lower_range = int(numbers[0])
            upper_range = int(numbers[1])
            if len(numbers) > 2:
                if len(numbers[2]) == 5:
                    zipcode = int(numbers[2])
                else:
                    unit = int(numbers[2])
            if len(numbers) > 3:
                if len(numbers[3]) == 5:
                    zipcode = int(numbers[3])
                else:
                    unit = int(numbers[3])
        elif numbers != None:
            lower_range = int(numbers[0])
            if len(numbers) > 1:
                if len(numbers[1]) == 5:
                    zipcode = int(numbers[1])
                else:
                    unit = int(numbers[1])
            if len(numbers) > 2:
                if len(numbers[2]) == 5:
                    zipcode = int(numbers[2])
                else:
                    unit = int(numbers[2])

        if unit == None:
            unit = letters[0].strip()

        name = re.findall('[a-zA-Z]{2,}', address)
        city = None
        if name != None:
            if len(name) > 1:
                city = name[1].lower()
            name = name[0].lower()
            if direction != None:
                name = direction + ' ' + name

        return {"lower_range": lower_range, "upper_range": upper_range, "street_name": name, "unit": unit, "city": city, "zipcode": zipcode}

    def compare_address(address1, address2):
        address1_components = get_address_components(address1)
        address2_components = get_address_components(address2)

        print(address1_components)
        print(address2_components)

        address1_lower = address1_components["lower_range"]
        address1_upper = address1_components["upper_range"]
        address2_lower = address2_components["lower_range"]
        address2_upper = address2_components["upper_range"]

        address1_unit = address1_components["unit"]
        address2_unit = address2_components["unit"]

        address1_street = address1_components["street_name"]
        address2_street = address2_components["street_name"]

        if address1_unit != None and address2_unit != None and address1_unit != address2_unit:
            return False
        elif address1_unit != None and address2_unit != None and address1_unit == address2_unit:
            unit = address1_unit
        elif address1_unit != None and address2_unit == None:
            unit = address1_unit
        elif address1_unit == None and address2_unit != None:
            unit = address2_unit
        elif address1_unit == None and address2_unit == None:
            unit = None

        if address1_street == address2_street:
            if address1_lower == address2_lower:
                return True, {"address": address1_lower, "street_name": address1_street, "unit": unit}
            elif address1_upper != None and address2_upper == None and address1_lower <= address2_lower and address2_lower <= address1_upper and address1_lower%2 == address2_lower%2:
                return True, {"address": address2_lower, "street_name": address1_street, "unit": unit}
            elif address2_upper != None and address1_upper == None and address2_lower <= address1_lower and address1_lower <= address2_upper and address1_lower%2 == address2_lower%2:
                return True, {"address": address1_lower, "street_name": address1_street, "unit": unit}
            else:
                return False
        else:
            return False
