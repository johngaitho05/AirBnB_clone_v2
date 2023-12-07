#!/usr/bin/env bash
# Script to configure Nginx server for serving web_static content

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/{releases/test,shared}
sudo chmod 755 /data/web_static/releases

# Create a fake HTML file for testing
echo "<html><head></head><body>Test Page</body></html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
nginx_alias="location /hbnb_static {\n\talias /data/web_static/current/;\n}"
if ! grep -q "location /hbnb_static" "$nginx_config"; then
    sudo sed -i "/server {/a $nginx_alias" "$nginx_config"
fi

# Restart Nginx to apply changes
sudo service nginx restart
