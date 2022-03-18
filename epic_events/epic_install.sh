#!/bin/bash

CURRENT_DIR=$(pwd)

echo "Epic Events will be installed here ${CURRENT_DIR}."
git clone https://github.com/AxAks/P12_Epic-Events.git
cd P12_Epic-Events

echo "The environment and requirements will now be installed..."
python3.9 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation of the Epic Events Database..."
sudo su postgres <<EOF
psql -c 'DROP DATABASE epiceventsdb;'
psql -c 'CREATE DATABASE epiceventsdb;'
psql -c 'CREATE USER django WITH PASSWORD 'djangepic';'
psql -c 'GRANT ALL PRIVILEGES on DATABASE epiceventsdb to django;'
EOF
exit

echo "Epic Events Installation successfully completed !"