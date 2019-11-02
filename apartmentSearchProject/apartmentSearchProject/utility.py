import requests as r
def setGeocoding(address):
    r.get("http://open.mapquestapi.com/geocoding/v1/address?key=vHLbcs1jwHWXH7wfuV8gEGi0wc83p3ON&location={{address}}")
    json = r.json
    latitude = json["results"][0]["locations"][0]["displayLatLng"]["latitude"]
    longitude = json["results"][0]["locations"][0]["displayLatLng"]["longitude"]
    return (latitude, longitude)

lat, lon = setGeocoding("581 Lear Road 44012")
print("Latitude: " + lat)
print("Longitude: " + lon)