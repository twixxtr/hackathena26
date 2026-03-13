#!/bin/bash

# This script deploys an Nginx reverse proxy configuration.
# It is called by the backend using pkexec so it runs entirely as root.

set -e

CONFIG_CONTENT="$1"
TARGET_PORT="$2"

if [ -z "$CONFIG_CONTENT" ] || [ -z "$TARGET_PORT" ]; then
    echo "Usage: ./deploy_nginx.sh <config_content> <target_port>"
    exit 1
fi

echo "[Deploy] Writing Nginx configuration for AI endpoint..."

# Write the config to a temporary file
TMP_CONF="/tmp/ai_protect_${TARGET_PORT}.conf"
echo "$CONFIG_CONTENT" > "$TMP_CONF"

# Install nginx and htpasswd utility if not present
if ! command -v nginx &> /dev/null; then
    echo "[Deploy] Installing Nginx..."
    apt-get update && apt-get install -y nginx apache2-utils
fi
if ! command -v htpasswd &> /dev/null; then
    apt-get install -y apache2-utils
fi

# Move the config to Nginx directory
mv "$TMP_CONF" /etc/nginx/sites-available/ai_protect
ln -sf /etc/nginx/sites-available/ai_protect /etc/nginx/sites-enabled/

# Remove default site to avoid port conflicts if we listen on 80/8080
rm -f /etc/nginx/sites-enabled/default

# Generate a default htpasswd file if it doesn't exist
if [ ! -f /etc/nginx/.htpasswd ]; then
    echo "[Deploy] Generating default admin credentials..."
    # The default password will be 'hackathon' mapped to user 'admin'
    htpasswd -cb /etc/nginx/.htpasswd admin hackathon
fi

# Restart Nginx
echo "[Deploy] Restarting Nginx service..."
systemctl restart nginx

echo "[Deploy] Successfully mitigated vulnerability. AI is now protected on port 8080."
