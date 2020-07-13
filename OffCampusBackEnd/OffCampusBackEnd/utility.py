import requests
import urllib
import json
import re
import math

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