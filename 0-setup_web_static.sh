#!/usr/bin/env bash
# Script to configure Nginx server for serving web_static content
#Install Nginx
sudo apt-get update
sudo apt-get install -y nginx
# Create folders
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
# Create a file with the HTML content
echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    Hbnb
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

#Create a semantic link
sudo ln -fs /data/web_static/releases/test/ /data/web_static/current
# Update file permissions
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i '39 i\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-enabled/default
sudo service nginx restart
