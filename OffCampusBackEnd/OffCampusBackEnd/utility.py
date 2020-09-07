import requests
import urllib
import json
import re
import math

def parse_address(address):  
    result = {}
    unknown = []

    # Certain items need to be removed from the address to avoid mismarking them address components
    address = address.replace(',', ' ')
    address = address.replace('.', ' ')
    address = address.replace('#', ' ')
    address = address.replace('Apt', ' ')
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
    if len(range) > 0 and 'street_range' not in result:
        addresses = re.findall('\d+', token)
        result['street_range'] = [addresses[0], addresses[1]]
        return

    # Prepare a regular expression to look for street names with numbers in the name.
    numbered_street = re.findall('\d+(st|nd|rd|th)', token, re.IGNORECASE)

    if token.isdigit():

        number_token = int(token)

        # Trying to find a zipcode.
        if len(token) == 5 and ('street_number' in result or 'street_range' in result):
            result['zipcode'] = token
            return

        # Looks for a range in the format 20 - 30.
        if len(tokens) >= 2 and tokens[0] == '-' and tokens[1].isdigit() and 'street_range' not in result:
            upper_address = int(tokens[1])
            result['street_range'] = [number_token, upper_address]
            tokens = tokens[2:]
            return

        # So we know we found the zip and range, so this can only be street number or unit.
        # Need to make sure that the street number is in the range provided otherwise it ain't it.
        # If it ain't a street number or unit, then we throw it in the wtf pile.
        if 'street_number' not in result:
            if 'street_range' not in result:
                result['street_number'] = token
                remove_duplicates('street_number', result, tokens)
            elif 'street_range' in result and int(result['street_range'][0]) <= number_token and number_token <= int(result['street_range'][1]):
                result['street_number'] = token
                remove_duplicates('street_number', result, tokens)
            elif 'unit' not in result:
                result['unit'] = token
                remove_duplicates('unit', result, tokens)
            else:
                unknown.append(token)
            return
        
        # It is possible that we get to this point, whatever string is left we chuck in the unit
        if 'unit' not in result:
            result['unit'] = token
            remove_duplicates('unit', result, tokens)

    elif token.isalpha():

        street_prefixes = ["north", "south", "east", "west", "n", "s", "e", "w", "mt", "mt.c"]
        street_types = ["avenue", "street", "road", "boulevard", "drive", "circle", "ave", "st", "rd", "blvd", "dr", "cir"]

        # Check if the string is a road direction
        if token.lower() in street_prefixes and 'street_name' not in result:
            result["street_prefix"] = token
            remove_duplicates('street_prefix', result, tokens)
            return

        # Check if the string is a road type
        if token.lower() in street_types:
            result["street_type"] = token
            remove_duplicates('street_type', result, tokens)
            return

        # Check if the string is a state or city.  This is pretty arbitrary for right now, but seems to work.
        if token.lower() in ["oh", "ohio"]:

            result['state'] = token
            return

        elif len(token) > 3 and 'street_name' in result:

            result['city'] = token
            return

        # Here we are going through the different combinations of a unit and street name being set.
        # I make the assumption that a street name must be long than two characters, which I think it a good assumption.
        # If the token is less than equal to two characters, we say that it is a unit
        # If we get to the end, we throw the token in the wtf pile.
        if 'street_name' not in result and 'unit' not in result and len(token) > 2:

            result['street_name'] = token
            remove_duplicates('street_name', result, tokens)

        elif 'street_name' not in result and 'unit' not in result and len(token) <= 2:

            result['unit'] = token
            remove_duplicates('unit', result, tokens)

        elif 'street_name' in result and 'unit' not in result:

            result['unit'] = token
            remove_duplicates('unit', result, tokens)

        elif 'street_name' not in result and 'unit' in result:

            result['street_name'] = token
            remove_duplicates('street_name', result, tokens)

        else:

            unknown.append(token)

    # Check to see if our numbered street regex found a numbers street
    elif len(numbered_street) > 0 and 'street_name' not in result:

        result['street_name'] = token
        remove_duplicates('street_name', result, tokens)

    # Again, here we just throw the junk in the unit
    elif 'unit' not in result and token.isalnum():

        result['unit'] = token
        remove_duplicates('unit', result, tokens)

    # Lastly, we throw everything else int the wtf pile.
    else:

        unknown.append(token)

    # Now we take a look at the unknowns to see if we can find a better representation of the unit.
    for token in unknown:
        if token.isalnum():
            if 'unit' in result and len(result['unit']) < len(token):
                unknown.append(result['unit'])
                result['unit'] = token
                unknown.remove(token)
            else:
                result['unit'] = token
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

    if 'street_number' not in address and 'street_range' not in address and 'unit' in address:
        address['street_number'] = address['unit']
        address.pop('unit')

    if ('street_prefix' in address) and  (address['street_prefix'].lower() in street_prefixes):
        address['street_prefix'] = street_prefixes[address['street_prefix'].lower()].lower().capitalize()
    elif 'street_prefix' in address:
        address['street_prefix'] = address['street_prefix'].lower().capitalize()

    address['street_name'] = address['street_name'].lower().capitalize()

    if 'street_type' in address and address['street_type'].lower() in street_types:
            address['street_type'] = street_types[address['street_type'].lower()].lower().capitalize()
    elif 'street_type' in address:
        address['street_type'] = address['street_type'].lower().capitalize()

    if 'city' in address:
        address['city'] = address['city'].lower().capitalize()

    if 'state' in address:
        if address['state'] == "OHIO":
            address['state'] = "OH"
        address['state'] = address['state'].upper()

    if 'unit' in address:
        address['unit'] = address['unit'].upper()

    string_address = ""

    if 'street_range' in address and 'street_number' not in address:
        string_address = string_address + f'{address["street_range"][0]} - {address["street_range"][1]}'
    elif 'street_number' in address:
        string_address = string_address + address['street_number']

    if 'street_prefix' in address:
        string_address = string_address + f' {address["street_prefix"]}'

    string_address = string_address + f' {address["street_name"]}'

    if 'street_type' in address:
        string_address = string_address + f' {address["street_type"]}'

    if 'city' in address:
        string_address = string_address + f', {address["city"]}'

    if 'state' in address:
        string_address = string_address + f' {address["state"]}'

    print("\n")
    print("STRING ADDRESS: " +  string_address)
    print("\n")
    return string_address, address

def getLatLong(address):
    query = {"key": "7a42def0c4b84b58a6bef95d82a82bcb", "q": address}
    r = requests.get('https://api.opencagedata.com/geocode/v1/json', params=query)
    o = r.json()
    latLongParent = o["results"][0]["geometry"]
    address = address[:address.find(", United States of America")]
    if latLongParent and "lat" in latLongParent:
        latitude = latLongParent["lat"]
        longitude = latLongParent["lng"]
        if (longitude < -90 or longitude > -70):
            latitude = None
            longitude = None
        return (latitude, longitude)
    return (None, None)

def distance(lat, lon):
    clocktower = (40.0049371,-83.012978)
    R = 6371e3 # meters
    loc = (lat, lon)
    clocktowerLatR = clocktower[0] / 180 * math.pi
    locLatR = lat / 180 * math.pi

    deltaLat = (clocktower[0] - loc[0]) / 180 * math.pi
    deltaLon = (clocktower[1] - loc[1]) / 180 * math.pi

    a = math.sin(deltaLat / 2) * math.sin(deltaLat / 2) + math.cos(locLatR) * math.cos(clocktowerLatR) * math.sin(deltaLon / 2) * math.sin(deltaLon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 0.000621371 # miles