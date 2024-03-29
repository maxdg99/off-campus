from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin
from OffCampusWebScrapers.scraper import Scraper
from OffCampusWebScrapers.appfolio import AppfolioScraper
from OffCampusRestApi.models import Listing


class HometeamAppfolioScraper:
    url = "https://ht.appfolio.com/listings"

    @classmethod
    def process_listings(cls, callback):
        AppfolioScraper.process_listings(HometeamAppfolioScraper.url, cls.__name__, callback)

class HometeamScraper(Scraper):

    url = "https://www.hometeamproperties.net/osu-off-campus-housing"

    @classmethod
    def process_listings(cls, callback):
        req = requests.get(url=HometeamScraper.url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        properties = soup.find("div", {"class": "grid"})
        listings = []

        for div in properties.findAll("div", recursive=False):
            listings.append(HometeamScraper.__dict_from_listing(cls, div))

        appfolio_listings = []
        HometeamAppfolioScraper.process_listings(lambda listing: appfolio_listings.append(listing))

        print("hometeam_listings: "+str(len(listings)))
        print("appfolio_listing: "+str(len(appfolio_listings)))
        for hometeam_listing in listings:
            for appfolio_listing in appfolio_listings:
                match, data = HometeamScraper.addresses_are_equal(hometeam_listing["address"], appfolio_listing["address"])
                if match:
                    if "bexely" in hometeam_listing["campus"].lower():
                        city = "Mansfield"
                    else:
                        city = "Columbus"

                    d = {"scraper": hometeam_listing["scraper"], "url": hometeam_listing["url"], "image": hometeam_listing["image"], "address": appfolio_listing["address"], "beds": hometeam_listing["beds"],
                        "baths": hometeam_listing["baths"], "price": appfolio_listing["price"], "availability_date": appfolio_listing["availability_date"], "availability_mode": appfolio_listing["availability_mode"], "active": True, "unit": appfolio_listing["unit"]}
                    
                    if data["unit"]:
                        d["unit"] = data["unit"]
                    
                    callback(d)

    def __dict_from_listing(cls, listingDiv):
            data = {}
            
            data["scraper"] = cls.__name__
            data["image"] = listingDiv.find("img")["src"]
            data["url"] = urljoin(HometeamScraper.url,
                                listingDiv.find("a")["href"])

            address = listingDiv.find("h4").text
            address = address[0:address.find(":")].strip()
            data["address"] = address

            campus = listingDiv.find_all("h4")[1]
            data["campus"] = campus.text

            bedbath = listingDiv.find("strong").text.split()

            data["beds"] = bedbath[0]
            data["baths"] = bedbath[2]

            data["price"] = None
            data["availability_date"] = None
            data["availability_mode"] = Listing.AvailabilityMode.NONE
            data["active"] = False

            return data

    def __get_address_components(address):
        # Purpose: This function parses an address for the hometeam website and the hometeam appfolio website

        # Assumptions: This function makes the assumption that the first thing in the address is the street_number

        # Convention: In the case that an address contains a range of street numbers, the numbers will be filled
        # accordingly in lower_range and upper_range.  In the case that an address contains one street number
        # or two addresses with an ampersand in between them, it wil be stored in lower_range.

        # Note: The city field may be innacurrate.  It is deduced by checking for any words left in the address after
        # everything else is parsed at so it is prone to bugs.  It is there in the case this code is used in other situations
        # where one site has properties from multiple cities.

        # Define some dictionaries to help us in conversions
        numeric_street_conversion = {"first": "1st", "second": "2nd", "third": "3rd", "fourth": "4th", "fifth": "5th", "sixth": "6th", "seventh": "7th", "eighth": "8th", "ninth": "9th", "tenth": "10th",
            "eleventh": "11th", "twelth": "12th", "thirteenth": "13th", "fourteenth": "14th", "fifteenth": "15th", "sixteenth": "16th", "seventeenth": "17th", "eighteenth": "18th", "ninteenth": "19th"}

        # For some reason, hometeam has bedrooms in address.  We must remove them
        # Get the reg exp matches
        bedroom = re.search(': \dBR(s)?', address)
        if bedroom != None:
            # Remove them from the string
            address = address.replace(bedroom, '')

        # Remove the word studio from any address
        if ': Studios' in address:
            address = address.replace(': Studios', '')

        if 'Apt' in address:
            address = address.replace('Apt', '')

        # Look for cardinal directions to replace
        direction_conversion = re.search(
            'North|South|East|West|NORTH|SOUTH|EAST|WEST|north|south|east|west|[., ]N[., ]|[., ]S[., ]|[., ]E[., ]|[., ]W[., ]', address)
        # If such a direcition exists replace it to lower case word format
        if direction_conversion != None:
            # Get the direction
            direction_conversion = direction_conversion[0]
            # Remove the direction from the address
            address = address.replace(direction_conversion, ' ')

            # Make the dirction lower case and remove punctuation and spaces
            direction_conversion = direction_conversion.replace(',', '')
            direction_conversion = direction_conversion.replace('.', '')
            address = address.replace(direction_conversion, ' ')
            direction_conversion = direction_conversion.lower()
            direction_conversion = direction_conversion.strip()

            # Convert abbreviations to words
            if 'n' == direction_conversion:
                direction_conversion = 'north'
            if 'e' == direction_conversion:
                direction_conversion = 'east'
            if 's' == direction_conversion:
                direction_conversion = 'south'
            if 'w' == direction_conversion:
                direction_conversion = 'west'

        # Look for road types and remove them if they exists.  They are relatively irrelevant
        road_type = re.search(
            'Avenue|Ave|Ave\.|Street|St|St\.|Road|Rd|Rd.', address, re.IGNORECASE)
        if road_type != None:
            road_type = road_type[0]
            address = address.replace(road_type, '')

        # Now, we look for the street names.  A minimum of 2 characters should suffice
        street_name = re.findall(
            '[a-zA-Z]{2,}|\d+TH|\d+ND|\d+RD|\d+ST', address, re.IGNORECASE)
        if len(street_name) > 0:
            # Get rid of the street name from the address
            address = address.replace(street_name[0], '')
            # Standardize the street name to lower case
            street_name = street_name[0].lower()
            # Make sure that we do not need to convert a word to a number
            if street_name in numeric_street_conversion:
                street_name = numeric_street_conversion[street_name]
            # If we have found a direction, add it back to the street name
            if direction_conversion != None:
                street_name = direction_conversion + ' ' + street_name

        # Here is where the fun starts!  Define a few regular expressions
        # Look for a range of address
        number_range = re.search('^\d+-\d+', address)
        # Get all numbers in the address
        numbers = re.findall('\d+', address)
        # Look if there is an address with an ampersand
        address_ampersand = re.search(
            '^\d*[a-zA-Z]?\d* ?& ?\d*[a-zA-Z]?\d*', address)
        # Get the letters in the address
        letters = re.findall('[., ]\d*[a-zA-Z]\d*[., ]', address)
        # Set all of the data points we want to None
        upper_range = lower_range = zipcode = unit = None

        # If the address has a range of street numbers
        if number_range != None and len(numbers) > 1:
            # This means that there must be a lower range and upper range
            lower_range = int(numbers[0])
            upper_range = int(numbers[1])
            # Then we remote the lower and upper range.  We are assuming they come first
            numbers.pop(0)
            numbers.pop(0)

            # Look for an ampersand of units
            unit_ampersand = re.search(
                '\d*[a-zA-Z]?\d* ?& ?\d*[a-zA-Z]?\d*', address)

            # If an ampersand exists in the unit, se
            if unit_ampersand != None:
                unit = unit_ampersand[0]

            # Look at each remaining number in the address and matche them to zipcodes, street numbers, or units
            for number in numbers:
                if lower_range and upper_range and lower_range <= int(number) and int(number) <= upper_range and lower_range %2 == int(number)%2:
                    lower_range = int(number)
                    upper_range = None
                # This may not be enough to check for a zipcode.  We will see
                elif len(number) == 5:
                    zipcode = int(number)
                else:
                    if unit == None:
                        unit = number
        elif address_ampersand != None:
            # Get the ampersand string and remove it
            lower_range = address_ampersand[0]
            address = address.replace(lower_range, '')

            # Calculate to see if there exists a unit ampersand after removing the first ampersand
            unit_ampersand = re.search(
                '\d*[a-zA-Z]?\d* ?& ?\d*[a-zA-Z]?\d*', address)

            # There are two numbers in our numbers array because there is an ampersand, remove them
            numbers.pop(0)
            numbers.pop(0)

            # If we have a unit ampersand set it
            if unit_ampersand != None:
                unit = unit_ampersand[0]

            # Sift through our numbers and match data points
            for number in numbers:
                # See if a number is a zip code
                if len(number) == 5:
                    zipcode = int(number)
                # Otherwise, set it as a unit if it has not already been set
                else:
                    if unit == None:
                        unit = number
        elif numbers != None and len(numbers) > 0:
            lower_range = int(numbers[0])
            numbers.pop(0)

            # Look for an ampersand of units
            unit_ampersand = re.search(
                '\d*[a-zA-Z]?\d* ?& ?\d*[a-zA-Z]?\d*', address)

            # Check if the unit has an ampersand
            if unit_ampersand != None:
                unit = unit_ampersand[0]

            # Look at the remaining numbers in the address and match them to units and zipcodes
            for number in numbers:
                if len(number) == 5:
                    zipcode = int(number)
                else:
                    if unit == None:
                        unit = number

        # If we do not have a unit yet, attmpept to match it to a letter
        if len(letters) > 0 and (unit == None or str(unit) in letters[0]):
            unit = letters[0].strip()

        # Get rid of any goofy stuff in the unit field
        if unit != None:
            unit = unit.replace(',', '')
            unit = unit.replace('.', '')
            unit = unit.replace(' ', '')

        # Return a well formed address parse
        return {"lower_range": lower_range, "upper_range": upper_range, "street_name": street_name, "unit": unit, "zipcode": zipcode}

    def addresses_are_equal(address1, address2):
        # Purpose: Compares two addresses by using get_address_components(string). Returns true and
        # a dictionary containing street number, street name, and unit if the units match.  Returns false
        # and an empty dictionary otherwise

        # Assumptions: If lower_range and upper_range are not null, then there is a range of address to
        # compare against.  An address matches in this range iff the given address is greater than the lower
        # limit, less than the upper limit, and the eveness/oddness matches that of the lower_range.  We also
        # assume that lower_range%2 =- upper_range%2.

        # Get the address components of each address
        address1_components = HometeamScraper.__get_address_components(address1)

        # Declare some variables to use as opposed to have to reference the dictionary every time
        address1_lower = address1_components["lower_range"]
        address1_upper = address1_components["upper_range"]
        address2_lower = address2["address_range"][0] if "address_range" in address2 else None
        address2_upper = address2["address_range"][1] if "address_range" in address2 else None

        address1_unit = address1_components["unit"]
        address2_unit = address2["unit"] if "unit" in address2 else None

        address1_street_name = address1_components["street_name"]
        address2_street_name = address2["street_name"]

        address1_zipcode = address1_components["zipcode"]
        address2_zipcode = address2["zipcode"] if "zipcode" in address2 else None

        unit = None

        # Check if the zipcodes match
        # If both addresses have a zip and they are equal, set it
        if address1_zipcode != None and address2_zipcode != None and address1_zipcode == address2_zipcode:
            zipcode = address1_zipcode
        # If one address has a zip and the other does not, set the zip to the one that does
        elif address1_zipcode != None and address2_zipcode == None:
            zipcode = address1_zipcode
        elif address1_zipcode == None and address2_zipcode != None:
            zipcode = address2_zipcode
        # If both do not have a zip, set zipcode to none
        elif address1_zipcode == None and address2_zipcode == None:
            zipcode = None
        # Otherwise, false
        else:
            return False, {}

        # If both addresses have a unit and they are equal, set it
        if address1_unit != None and address2_unit != None and address1_unit == address2_unit:
            unit = address1_unit
        # If one address has a unit and the other does not, set the unit to the one that does
        elif address1_unit != None and address2_unit == None:
            unit = address1_unit
        elif address1_unit == None and address2_unit != None:
            unit = address2_unit
        elif address1_unit == None and address2_unit == None:
            unit = None
        else:
            return False, {}

        # Check if the street names match
        if address1_street_name == address2_street_name:
            # If the lowers are equal to each other, then we have an automatic match
            if address1_lower == address2_lower:
                return True, {"street_number": address1_lower, "street_name": address1_street_name, "unit": unit, "zipcode": zipcode}
            # Check if each address is in the range of the other, if so true
            elif address1_upper != None and address2_upper == None and address1_lower <= address2_lower and address2_lower <= address1_upper and address1_lower %2 == address2_lower%2:
                return True, {"street_number": address2_lower, "street_name": address1_street_name, "unit": unit, "zipcode": zipcode}
            elif address2_upper != None and address1_upper == None and address2_lower <= address1_lower and address1_lower <= address2_upper and address1_lower %2 == address2_lower%2:
                return True, {"street_number": address1_lower, "street_name": address1_street_name, "unit": unit, "zipcode": zipcode}
            # Otherwise, false
            else:
                return False, {}
        # If the street names do not match, false
        else:
            return False, {}
