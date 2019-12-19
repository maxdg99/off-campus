# Background
This started as Max Gruber, Andrew Haberlandt, and Adam Lis's Hack OHI/O 2019 project. It is a web app and web scraper that allows the user to view aggregated property data from various realties around the campus of The Ohio State University.

# Getting up and running
1. Python
    1. Install Python 3
    1. Install pip
    1. Install Django: `pip install django`
    1. Install Requests: `pip install requests`
    1. Install Beautiful Soup 4: `pip install bs4`
    1. Install python-dotenv: `pip install python-dotenv`
1. Vue.js
    1. Install npm
    1. Install Vue.js: `npm install vue`
    1. Install the dependencies in the Vue project: `npm install`
1. Back end
    1. Navigate to the OffCampusBackEnd directory
    1. Copy sample-db.sqlite3 and rename it to db.sqlite3
    1. Run the Django app with this command: `python manage.py runserver`
1. Front end
    1. Navigate to the off-campus-front-end directory
    1. Run the Vue app with this command: `npm run serve`
