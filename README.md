# Background
This started as Max Gruber, Andrew Haberlandt, and Adam Lis's Hack OHI/O 2019 project. It is a web app and web scraper that allows the user to view aggregated property data from various realties around the campus of The Ohio State University.

# Getting up and running
1. Install Python 3
    1. Install Django
    1. Install Requests
    1. Install Beautiful Soup 4
1. Install Vue.js
    1. Install the dependencies in off-campus-front-end/package.json
1. Run the back end
    1. Navigate to the OffCampusBackEnd directory
    1. Copy sample-db.sqlite3 and rename it to db.sqlite3
    1. Run the Django app with this command: `python manage.py runserver`
1. Run the front end
    1. Navigate to the off-campus-front-end directory
    1. Run the Vue app with this command: `npm run serve`
