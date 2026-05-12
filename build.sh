#!/bin/bash
# Install system dependencies for Chromium
apt-get update
apt-get install -y chromium-browser

# Install Python dependencies
pip install -r requirements.txt