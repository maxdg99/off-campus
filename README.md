# Off Campus

This started as Max Gruber, Andrew Haberlandt, and Adam Lis's Hack OHI/O 2019 project. It is a web app and web scraper that allows the user to view aggregated property data from various realties around the campus of The Ohio State University.

## Setting up the app

1. Install dependencies: `sudo apt install build-essential postgresql libpq-dev python3 python3-pip nodejs npm`
1. Set up back end
    1. Navigate to the back end directory
    1. Install the dependencies in the Django project: `pip install -r requirements.txt`
    1. Set up the environment variables file
        1. Copy .env.local.example and rename it to .env.local
        1. Populate the "SECRET_KEY"
        1. Populate the "GOOGLE_SECRET_KEY"
    1. Run Django migrations: `python manage.py migrate`
    1. Scrape listings: `python manage.py scrape`
1. Set up database
    1. Start the Postgres service: `sudo service postgresql start`
    1. Change the password of the postgres user
        1. Open psql: `sudo -u postgres psql`
        1. Change the password: `\password postgres`
        1. Quit psql: `\q`
    1. Update the password of the postgres user in the backend .env file
        1. Navigate to the backend directory
        1. Open the .env file
        1. Change the "POSTGRES_PASSWORD" to the password you set above
    1. Create the Off Campus database: `sudo -u postgres createdb offcampus`
    1. Change Postgres's authentication mode
        1. Find the configuration file: `sudo -u postgres psql -c "show hba_file;"`
        1. Open the configuration file: `sudo vim [configuration file path]`
        1. Change "md5" to "password" in these lines:
            ```
            # IPv4 local connections:
            host    all             all             127.0.0.1/32            md5
            # IPv6 local connections:
            host    all             all             ::1/128                 md5
            ```
1. Set up front end
    1. Navigate to the front end directory
    1. Install the dependencies in the Vue project: `npm install`

## Running the app

1. Navigate to the back end directory and run the Django app: `python manage.py runserver`
1. Navigate to the front end directory and run the Vue app: `npm run serve`
