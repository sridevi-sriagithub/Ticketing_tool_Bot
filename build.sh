# pip install -r requirements.txt
# pip install botbuilder-core==4.14.0 botbuilder-schema==4.14.0 botbuilder-dialogs==4.14.0 aiohttp --no-deps


#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing Bot Framework packages..."
pip install botbuilder-core==4.14.0 \
           botbuilder-schema==4.14.0 \
           botbuilder-dialogs==4.14.0 \
           aiohttp \
           msrest --no-deps

echo "Build completed!"
