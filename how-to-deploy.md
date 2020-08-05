How to deploy using uwsgi (suitable for production
====

We will be using /opt/apartments/ for our stuff. Why? idk.

Right now I'm using a t2.micro on AWS. Ubuntu 18.04.

Install shit
------
```
sudo apt update
sudo apt install python3 python3-pip nginx npm
sudo pip3 install --system uwsgi
# ...wait patiently...
sudo npm install -g npm@3
hash -d npm
```

Generate SSH Key
-----
```
ssh-keygen
# Default location is fine
# USE A GOOD PASSWORD
```

Now, paste the output of the following command in your Github SSH keys section

MUCH MORE SECURE WAY: Add it as a deploy key for this repo (annoyingly we don't have permission to, because Supreme Overlord Max)
```
cat ~/.ssh/id_rsa.pub 
```


More stuff
-------
```
sudo useradd apartments
sudo usermod -a -G apartments ubuntu
sudo usermod -a -G apartments www-data
sudo mkdir /opt/apartments
sudo chown apartments:apartments /opt/apartments
sudo chmod 775 /opt/apartments
sudo mkdir /opt/apartments/sock
sudo chown apartments:apartments /opt/apartments/sock
sudo chmod 774 /opt/apartments/sock

# Log out and log back in before continuing.
cd /opt/apartments/
git clone git@github.com:maxdg99/Apartment-Web-Scraper.git app
sudo chown -R apartments:apartments app
virtualenv -p python3 venv
source venv/bin/activate
cd app/OffCampusBackEnd
pip install -r requirements.txt
pip install -r requirements-deploy.txt 

sudo mkdir -p /etc/uwsgi/vassals/
sudo cp production_uwsgi.ini /etc/uwsgi/vassals/

cd ../off-campus-front-end
npm install
npm run build
# ... wait patiently ...
```

More more stuff
-----

Put the following in /etc/systemd/system/uwsgi.service (you'll need sudo)
```
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

Write the following to /etc/nginx/sites-available/apartments-front
```
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

Write the following to /etc/nginx/sites-available/apartments-api

```
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

now run:
```
sudo ln -s /etc/nginx/sites-available/apartments-api /etc/nginx/sites-enabled/apartments-api
sudo ln -s /etc/nginx/sites-available/apartments-front /etc/nginx/sites-enabled/apartments-front
```

Put the following in /opt/apartments/app/OffCampusBackEnd/.env.local
```
SECRET_KEY=^f)iru73nvws+!1#^3xf3wl2tu&y+$9yk=v^j@_tc+v7^d&a^f
DEBUG=false
```

Now run:
```
sudo systemctl daemon-reload
sudo systemctl start uwsgi


