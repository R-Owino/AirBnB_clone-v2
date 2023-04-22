#!/usr/bin/env bash
# script that sets up the web servers for the deployment of web_static

# Update package list
sudo apt-get -y update

# Install Nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get install nginx -y
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared /data/web_static/current

# Create a fake HTML file to test Nginx configuration
sudo echo "<html><head><title>Test Page</title></head><body><p>This is a test page</p></body></html>" | sudo tee /data/web_static/releases/test/index.html

# Set ownership and permissions
sudo chown -R ubuntu:ubuntu /data/
sudo chgrp -R ubuntu /data/

# Remove existing symbolic link if it exists
sudo rm -rf /data/web_static/current

# Create new symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Configure Nginx to serve web_static
server_config="server {
		listen 80 default_server;
		listen [::]:80 default_server;
		root /var/www/html;
		index index.html index.htm;
		server_name _;
		add_header X-Served-By \$hostname;
		location /hbnb_static {
			alias /data/web_static/current;
			index index.html index.htm;
		}
		location /redirect_me {
			return 301 https://rupert.id.au/python/book/learn-python3-the-hard-way-nov-15-2018.pdf;
		}
		error_page 404 /404.html;
		location = /404.html {
			internal;
		}
	}"

echo -e "$server_config" > /etc/nginx/sites-available/default

# Restart nginx
sudo service nginx restart
