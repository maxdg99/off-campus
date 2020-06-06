from bs4 import BeautifulSoup
import requests
from OffCampusWebScrapers.scraper import Scraper
import datetime
import re

class KRGScraper(Scraper):
    @staticmethod
    def _remove_special_chars(string):
        chars = ['"', '$', ' ', '<br>', 'Bedrooms:', 'Bathrooms:', '\\']
        for char in chars:
            string = string.replace(char, '')
        return string

    @classmethod
    def process_listings(cls, callback):  
        req_url = "https://krg.ua.rentmanager.com/search_result?rmwebsvc_command=Search_Result.aspx&rmwebsvc_template=unitlist&rmwebsvc_Page=1&rmwebsvc_start=10&rmwebsvc_corpid=krg&rmwebsvc_mode=&rmwebsvc_locations=1"
        req = requests.get(url=req_url, headers={"User-Agent": "Mozilla/5.0"})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find('div', {'class', 'NavigationPage'}).text
        pages = int(re.findall('\d+', pages)[1])

        for page in range(1, pages):
            req_url = f'https://krg.ua.rentmanager.com/search_result?rmwebsvc_command=Search_Result.aspx&rmwebsvc_template=unitlist&rmwebsvc_Page={page}&rmwebsvc_start={page*10}&rmwebsvc_corpid=krg&rmwebsvc_mode=&rmwebsvc_locations=1'
            req = requests.get(url=req_url, headers={"User-Agent": "Mozilla/5.0"})
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            pages = soup.find('div', {'class', 'NavigationPage'}).te

            table = soup.find('table')
            listings = table.find_all('td')
            for listing in listings:
                url = "https://krgre.com" + KRGScraper._remove_special_chars(listing.find('a')['href'])
                url = url.replace('rmwebsvc_mode=', 'rmwebsvc_mode=javascript')
                image = KRGScraper._remove_special_chars(listing.find('img')['src'])
                address = listing.find('div', {'class': '\\\"address\\\"'}).text.replace('"', '')

                price = listing.find('div', {'class': '\\\"rent\\\"'}).text
                price = price.replace('$', '')
                price = price.replace(',', '')
                price = price.replace('.00', '')
                price = int(price)

                beds = int(listing.find_all('span', {'class': '\\\"info-value\\\"'})[0].text)
                baths = float(listing.find_all('span', {'class': '\\\"info-value\\\"'})[1].text)

                availability = listing.find_all('span', {'class': '\\\"info-title\\\"'})[2].text
                avail_mode = 'None'
                avail_date = None
                if 'NOW' in availability or 'Now' in availability:
                    avail_date = None
                    avail_mode = 'Now'
                elif 'Application Pending' not in availability and len(availability) > 0:
                    if '/' in availability:
                        try:
                            avail_date = datetime.datetime.strptime(availability, "%m/%d/%Y").date()
                        except ValueError:
                            avail_date = datetime.datetime.strptime(availability, "%m/%d/%y").date()
                    elif ',' in availability:
                        avail_date = datetime.datetime.strptime(availability, "%B %d, %Y").date()
                    else:
                        avail_date = datetime.datetime.strptime(availability, "%M%d%Y").date()
                    avail_mode = 'Date'

                d = {"scraper": cls.__name__, "url": url, "image": image, "address": address, "beds": beds, "baths": baths, "price": price, "availability_date": avail_date, "availability_mode": avail_mode, "active": True}
                print(d)
                #callback(d)
