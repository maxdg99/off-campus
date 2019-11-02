from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from scrapers.scraper import Scraper

class HometeamScraper(Scraper):
    hometeamURL = "https://www.hometeamproperties.net/osu-off-campus-housing"
    northsteppeURL = "https://northsteppe.appfolio.com/listings?1572716642290&filters%5Bproperty_list%5D=All%20OSU%20Campus%20Area%20Properties&theme_color=%23194261&filters%5Border_by%5D=date_posted"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def dict_from_listing(listingDiv):
        l = {}
        l["image_url"] = listingDiv.find("img")["src"]
        l["url"] = urljoin(HometeamScraper.hometeamURL, listingDiv.find("a")["href"])
        l["address"] = listingDiv.find("h4").text

        bedbath = listingDiv.find("strong").text.split()
        l["num_bedrooms"] = bedbath[0]
        l["num_bathrooms"] = bedbath[2]

        l["active"] = True

        return l

    def process_listings(callback):
        ht = requests.get(url=HometeamScraper.hometeamURL)
        htHTML = ht.text
        htSoup = BeautifulSoup(htHTML, 'html.parser')
        htProperties = htSoup.find("div", {"class": "grid"})
        for listingDiv in htProperties.findAll("div", recursive=False):
            callback(HometeamScraper.dict_from_listing(listingDiv))