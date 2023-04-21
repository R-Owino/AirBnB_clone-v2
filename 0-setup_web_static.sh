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
sudo sed -i '48i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
sudo service nginx restart
