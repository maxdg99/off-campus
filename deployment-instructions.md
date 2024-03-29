# First-time deployment
These instructions have been tested on an AWS t2.micro with Ubuntu 18.04. Our code will go in /opt/apartments/ because Andrew said so. 

## Install dependencies
```sh
sudo apt update
sudo apt install python3 python3-pip nginx npm virtualenv snap
# This will take a while
sudo pip3 install --system uwsgi
sudo npm install -g npm@3
```

## Generate SSH Key
```sh
ssh-keygen
# Use default location
# USE A GOOD PASSWORD
cat ~/.ssh/id_rsa.pub 
```

Paste the output into GitHub
* More secure way: add as deployment key for this repo
* Less secure way: add to GitHub account SSH keys


## Set up apartments user
```sh
sudo useradd apartments
sudo usermod -a -G apartments ubuntu
sudo usermod -a -G apartments www-data
sudo mkdir /opt/apartments
sudo chown apartments:apartments /opt/apartments
sudo chmod 775 /opt/apartments
sudo mkdir /opt/apartments/sock
sudo chown apartments:apartments /opt/apartments/sock
sudo chmod 774 /opt/apartments/sock
# Log out and log back in before continuing
```

## Clone and build project
```sh
cd /opt/apartments/
git clone git@github.com:maxdg99/Apartment-Web-Scraper.git app
sudo chown -R apartments:apartments app

virtualenv -p python3 venv
source venv/bin/activate
cd app/OffCampusBackEnd
pip install -r requirements.txt
pip install -r requirements-deploy.txt
python manage.py migrate
python manage.py scrape
deactivate

sudo mkdir -p /etc/uwsgi/vassals/
sudo cp production_uwsgi.ini /etc/uwsgi/vassals/

# This will take a while
cd ../off-campus-front-end
npm install
npm run build
```

## Set up configuration files
Write the following to /etc/systemd/system/uwsgi.service (using sudo)
```nginx
[Unit]
Description=Apartments uWSGI Emperor
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
# Requires systemd version 211 or newer
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

Write the following to /etc/nginx/sites-available/apartments-front (using sudo)
```nginx
server {
	root /opt/apartments/app/off-campus-front-end/dist;
	index index.html index.htm index.nginx-debian.html;
  server_name offcampus.us;

  location / {
    index  index.html;
    try_files $uri $uri/ /index.html;
  }
  error_page   500 502 503 504  /50x.html;
  location = /50x.html {
    root   /usr/share/nginx/html;
  }
}
```

Write the following to /etc/nginx/sites-available/apartments-api (using sudo)
```nginx
# the upstream component nginx needs to connect to
upstream django {
  server unix:///opt/apartments/sock/apartments.sock; # for a file socket
}

# configuration of the server
server {
  # the port your site will be served on
  # the domain name it will serve for
  server_name api.offcampus.us; # substitute your machine's IP address or FQDN
  charset     utf-8;

  # max upload size
  client_max_body_size 1M;   # adjust to taste

  # Finally, send all non-media requests to the Django server.
  location / {
     uwsgi_pass  django;
     include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
  }

}
```

Write the following to /opt/apartments/app/OffCampusBackEnd/.env.local (inserting a secure secret key where prompted to do so)
```sh
SECRET_KEY=INSERT SECURE SECRET KEY HERE
DEBUG=false
HOST_URL=api.offcampus.us
```

## Finish setup
```sh
sudo ln -s /etc/nginx/sites-available/apartments-api /etc/nginx/sites-enabled/apartments-api
sudo ln -s /etc/nginx/sites-available/apartments-front /etc/nginx/sites-enabled/apartments-front

sudo service nginx restart

sudo snap install --classic certbot
sudo certbot --nginx
# Enter your email to be notified about certificate expirations

sudo systemctl daemon-reload
sudo systemctl start uwsgi
```

You're done! Everything should be up and running.

# Normal deployment
1. Stop application: `sudo systemctl stop uwsgi`
1. Navigate to repository: `cd /opt/apartments/app`
1. Pull new code: `git pull`
1. Navigate to back end directory: `cd OffCampusBackEnd`
1. Delete Django database *if necessary*: `rm db.sqlite3`
1. Enter virtual environment: `source /opt/apartments/venv/bin/activate`
1. Run Django migrations: `python manage.py migrate`
1. Run Django scrapers: `python manage.py scrape`
1. Exit virtual environment: `deactivate`
1. Navigate to front end directory: `cd ../off-campus-front-end`
1. Rebuild front end:
	```
	npm install
	npm run build
	```
1. Restart application:	`sudo systemctl start uwsgi`

# Troubleshooting
* View UWSGI logs: `sudo journalctl -u uwsgi -f`
* Database is read-only:
	```
	sudo chown apartments:apartments db.sqlite3
	sudo chmod 664
	```
