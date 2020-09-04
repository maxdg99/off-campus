import requests
import urllib
import json
import re
import math

def getLatLong(address):
    to_find = re.compile("Street|St|Avenue|Ave|Road|Rd")
    match = to_find.search(address)
    if match:
        idx = address.find(",")
        if idx != match.end() and ',' in address:
            print("before: "+address)
            address = address[0:match.end()] + address[idx:]
            print("after "+address)


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
    westBound = -83.025 # 1. Anyone West of this is considered West Campus
    southBound = 39.995 # 2. Anyone South of this is considered South Campus
    northBound = 40.006 # 3. Anyone North of this is considered North Campus
    eastBound = -83.009 # 4. Anyone East of this is considered 'East Campus' (University District)

    if lon < westBound:
        return 'west'
    elif lat < southBound:
        return 'south'
    elif lat > northBound:
        return 'north'
    else:
        return 'east'

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
            print(address)

    zipcode = re.search("\d{5}", address)
    if zipcode:
        address = address.replace(zipcode[0], " ")

    address = address.replace(",", "")

    return address