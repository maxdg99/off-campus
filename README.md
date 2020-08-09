# Off Campus

This started as Max Gruber, Andrew Haberlandt, and Adam Lis's Hack OHI/O 2019 project. It is a web app and web scraper that allows the user to view aggregated property data from various realties around the campus of The Ohio State University.

## Getting up and running

1. Back end
    1. Install [Python 3](https://www.python.org/downloads/)
    1. Navigate to the `OffCampusBackEnd` directory
    1. Install the dependencies in the Django project: `pip install -r requirements.txt`
    1. Copy `sample-db.sqlite3` and rename it to `db.sqlite3`
    1. Create `.env.local` and populate it as follow: `SECRET_KEY={insert secret key here}`
    1. Run the Django app with this command: `python manage.py runserver`
1. Front end
    1. Install [Node.js](https://nodejs.org/)
    1. Navigate to the `off-campus-front-end` directory
    1. Install the dependencies in the Vue project: `npm install`
    1. Run the Vue app with this command: `npm run serve`
