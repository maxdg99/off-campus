from bs4 import BeautifulSoup
import requests
from OffCampusWebScrapers.scraper import Scraper
import datetime
import re

class EdwardsScraper(Scraper):

    def process_listings(req_url, cls, callback):  
        req = requests.get(url=req_url, headers={"User-Agent": "Mozilla/5.0"})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        rooms = soup.find_all('div', {'class', 'floorplan-tile ng-scope'})

        address = soup.find('div', {'class': 'address'})
        address.find('a').decompose()
        address = address.text
        address = address[address.index('\n'):].strip()

        print(html)

        for room in rooms:
            info = room.find('div', {'class': 'specs ng-binding'})
            info_re = re.find_all('/d+', info)
            beds = info_re[0]
            baths = info_re[1]
            print(beds)

class DoricScraper(Scraper):
    url = "https://2301843v3.onlineleasing.realpage.com/#k=97230"

    @classmethod
    def process_listings(cls, callback):
        EdwardsScraper.process_listings(DoricScraper.url, cls.__name__, callback)