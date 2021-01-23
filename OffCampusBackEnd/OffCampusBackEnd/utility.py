import requests
import urllib
import json
import re
import math
import os
from OffCampusRestApi.models import Listing

STREET_RANGE = 'street_range'
STREET_NUMBER = 'street_number'
UNIT = 'unit'
STREET_NAME = 'street_name'
STREET_PREFIX = 'street_prefix'
STREET_TYPE = 'street_type'
CITY = 'city'
STATE = 'state'

def parse_address(address):  
    result = {}
    unknown = []

    # Certain items need to be removed from the address to avoid mismarking them address components
    address = address.replace(',', ' ')
    address = address.replace('.', ' ')
    address = address.replace('#', ' ')
    address = address.replace('Apt', ' ')
    address = address.replace('APT', ' ')
    address = address.replace('Apartment', ' ')
    address = address.replace('Unit', ' ')
    address = address.replace('(OSU)', ' ')

    tokens = address.split(' ')
    
    while len(tokens) > 0:
        token = tokens.pop(0)

        handle_token(token, tokens, unknown, result)

    return result, unknown

def handle_token(token, tokens, unknown, result):

    # Looks for a range denoted like 10-20.
    range = re.findall('\d+[-]\d+', token)
    if len(range) > 0 and STREET_RANGE not in result:
        addresses = re.findall('\d+', token)
        result[STREET_RANGE] = [addresses[0], addresses[1]]
        return

    # Prepare a regular expression to look for street names with numbers in the name.
    numbered_street = re.findall('\d+(st|nd|rd|th)', token, re.IGNORECASE)

    if token.isdigit():

        number_token = int(token)

        # Trying to find a zipcode.
        if len(token) == 5 and (STREET_NUMBER in result or STREET_RANGE in result):
            result['zipcode'] = token
            return

        # Looks for a range in the format 20 - 30.
        if len(tokens) >= 2 and tokens[0] == '-' and tokens[1].isdigit() and STREET_RANGE not in result:
            upper_address = int(tokens[1])
            result[STREET_RANGE] = [number_token, upper_address]
            tokens = tokens[2:]
            return

        # So we know we found the zip and range, so this can only be street number or unit.
        # Need to make sure that the street number is in the range provided otherwise it ain't it.
        # If it ain't a street number or unit, then we throw it in the wtf pile.
        if STREET_NUMBER not in result:
            if STREET_RANGE not in result:
                result[STREET_NUMBER] = token
                remove_duplicates(STREET_NUMBER, result, tokens)
            elif STREET_RANGE in result and int(result[STREET_RANGE][0]) <= number_token and number_token <= int(result[STREET_RANGE][1]):
                result[STREET_NUMBER] = token
                remove_duplicates(STREET_NUMBER, result, tokens)
            elif UNIT not in result:
                result[UNIT] = token
                remove_duplicates(UNIT, result, tokens)
            else:
                unknown.append(token)
            return
        
        # It is possible that we get to this point, whatever string is left we chuck in the unit
        if UNIT not in result:
            result[UNIT] = token
            remove_duplicates(UNIT, result, tokens)

    elif token.isalpha():

        street_prefixes = ["north", "south", "east", "west", "n", "s", "e", "w", "mt", "mt.c"]
        street_types = ["avenue", "street", "road", "boulevard", "drive", "circle", "ave", "st", "rd", "blvd", "dr", "cir"]

        # Check if the string is a road direction
        if token.lower() in street_prefixes and STREET_NAME not in result:
            result[STREET_PREFIX] = token
            remove_duplicates(STREET_PREFIX, result, tokens)
            return

        # Check if the string is a road type
        if token.lower() in street_types:
            result[STREET_TYPE] = token
            remove_duplicates(STREET_TYPE, result, tokens)
            return

        # Check if the string is a state or city.  This is pretty arbitrary for right now, but seems to work.
        if token.lower() in ["oh", "ohio"]:

            result[STATE] = token
            return

        elif len(token) > 3 and STREET_NAME in result:

            result[CITY] = token
            return

        # Here we are going through the different combinations of a unit and street name being set.
        # I make the assumption that a street name must be long than two characters, which I think it a good assumption.
        # If the token is less than equal to two characters, we say that it is a unit
        # If we get to the end, we throw the token in the wtf pile.
        if STREET_NAME not in result and UNIT not in result and len(token) > 2:

            result[STREET_NAME] = token
            remove_duplicates(STREET_NAME, result, tokens)

        elif STREET_NAME not in result and UNIT not in result and len(token) <= 2:

            result[UNIT] = token
            remove_duplicates(UNIT, result, tokens)

        elif STREET_NAME in result and UNIT not in result:

            result[UNIT] = token
            remove_duplicates(UNIT, result, tokens)

        elif STREET_NAME not in result and UNIT in result:

            result[STREET_NAME] = token
            remove_duplicates(STREET_NAME, result, tokens)

        else:

            unknown.append(token)

    # Check to see if our numbered street regex found a numbers street
    elif len(numbered_street) > 0 and STREET_NAME not in result:

        result[STREET_NAME] = token
        remove_duplicates(STREET_NAME, result, tokens)

    # Again, here we just throw the junk in the unit
    elif UNIT not in result and token.isalnum():

        result[UNIT] = token
        remove_duplicates(UNIT, result, tokens)

    # Lastly, we throw everything else int the wtf pile.
    else:

        unknown.append(token)

    # Now we take a look at the unknowns to see if we can find a better representation of the unit.
    for token in unknown:
        if token.isalnum():
            if UNIT in result and len(result[UNIT]) < len(token):
                unknown.append(result[UNIT])
                result[UNIT] = token
                unknown.remove(token)
            else:
                result[UNIT] = token
                unknown.remove(token)

def remove_duplicates(key, result, tokens):
    if result[key] in tokens:
        tokens.remove(result[key])

def standardize_address(address):
    street_prefixes = {
        "north": "n",
        "south": "s",
        "east": "e",
        "west": "w" 
    }

    street_types = {
        "avenue": "ave",
        "street": "st",
        "road": "rd",
        "boulevard": "blvd",
        "drive": "dr",
        "circle": "cir"
    }

    if STREET_NUMBER not in address and STREET_RANGE not in address and UNIT in address:
        address[STREET_NUMBER] = address[UNIT]
        address.pop(UNIT)

    if (STREET_PREFIX in address) and  (address[STREET_PREFIX].lower() in street_prefixes):
        address[STREET_PREFIX] = street_prefixes[address[STREET_PREFIX].lower()].lower().capitalize()
    elif STREET_PREFIX in address:
        address[STREET_PREFIX] = address[STREET_PREFIX].lower().capitalize()

    address[STREET_NAME] = address[STREET_NAME].lower().capitalize()

    if STREET_TYPE in address and address[STREET_TYPE].lower() in street_types:
            address[STREET_TYPE] = street_types[address[STREET_TYPE].lower()].lower().capitalize()
    elif STREET_TYPE in address:
        address[STREET_TYPE] = address[STREET_TYPE].lower().capitalize()

    if CITY in address:
        address[CITY] = address[CITY].lower().capitalize()

    if STATE in address:
        if address[STATE] == "OHIO":
            address[STATE] = "OH"
        address[STATE] = address[STATE].upper()

    if UNIT in address:
        address[UNIT] = address[UNIT].upper()

    string_address = ""

    if STREET_RANGE in address and STREET_NUMBER not in address:
        string_address = string_address + f'{address[STREET_RANGE][0]} - {address[STREET_RANGE][1]}'
    elif STREET_NUMBER in address:
        string_address = string_address + address[STREET_NUMBER]

    if STREET_PREFIX in address:
        string_address = string_address + f' {address[STREET_PREFIX]}'

    string_address = string_address + f' {address[STREET_NAME]}'

    if STREET_TYPE in address:
        string_address = string_address + f' {address[STREET_TYPE]}'

    if CITY in address:
        string_address = string_address + f', {address[CITY]}'

    if STATE in address:
        string_address = string_address + f' {address[STATE]}'

    # print("\n")
    # print("STRING ADDRESS: " +  string_address)
    # print("\n")
    return string_address, address

def getLatLong(address):
    print(address)
    query = {"key": os.getenv("GOOGLE_SECRET_KEY"), "address": address}
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=query)
    o = r.json()
    print(o)
    latLongParent = o["results"][0]["geometry"]["location"]
    if latLongParent and "lat" in latLongParent:
        latitude = latLongParent["lat"]
        longitude = latLongParent["lng"]
        if (longitude < -90 or longitude > -70):
            latitude = None
            longitude = None
        return (latitude, longitude)
    return (None, None)

def distance(lat, lon):
    keypoint = (40.0016731,-83.0156426) # Currently: 18th Ave Library
    R = 6371e3 # meters
    loc = (lat, lon)
    keypointLatR = keypoint[0] / 180 * math.pi
    locLatR = lat / 180 * math.pi

    deltaLat = (keypoint[0] - loc[0]) / 180 * math.pi
    deltaLon = (keypoint[1] - loc[1]) / 180 * math.pi

    a = math.sin(deltaLat / 2) * math.sin(deltaLat / 2) + math.cos(locLatR) * math.cos(keypointLatR) * math.sin(deltaLon / 2) * math.sin(deltaLon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 0.000621371 # miles

def get_region(lat, lon):
    thompsonLibraryLatitude = 39.99925
    laneAndHighLongitude = -83.00936
    kingAndCanonLongitude = -83.02211

    if lat > thompsonLibraryLatitude:
        if lon < kingAndCanonLongitude:
            result = Listing.CampusArea.NORTHWEST
        elif lon > laneAndHighLongitude:
            result = Listing.CampusArea.NORTHEAST
        else:
            result = Listing.CampusArea.NORTH
    else:
        if lon < kingAndCanonLongitude:
            result = Listing.CampusArea.SOUTHWEST
        elif lon > laneAndHighLongitude:
            result = Listing.CampusArea.SOUTHEAST
        else:
            result = Listing.CampusArea.SOUTH
    
    return result

def format_address(address):
    replacements = {
        " North": " N. ",
        " East": " E. ",
        " South": " S. ",
        " West": " W. ",
        " Rd": " Road ",
        " St": " Street ",
        " Ave": " Avenue ",
        " Columbus": "",
        " Mansfield": "",
        " OH": ""
    }

    modifiers = [".", ",", " "]

    for key in replacements:
        for mod in modifiers:
            address_re = re.compile(re.escape(key+mod), re.IGNORECASE)
            address = address_re.sub(replacements[key], address)

    zipcode = re.search("\d{5}", address)
    if zipcode:
        address = address.replace(zipcode[0], " ")

    address = address.replace(",", "")

    return address