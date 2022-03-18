#!/bin/bash

echo "Epic Events Installation."
echo "The environment and requirements will now be installed..."
python3.9 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation of the Epic Events Database..."
sudo su postgres <<EOF
service postgresql restart
psql -c 'DROP DATABASE epicdb;'
psql -c 'CREATE DATABASE epicdb;'
psql -c "CREATE USER epicuser WITH PASSWORD 'djangepic';"
psql -c 'GRANT ALL PRIVILEGES on DATABASE epicdb to epicuser;'
EOF
exit

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata core/fixture/departments_fixtures.json

echo "Epic Events Installation successfully completed !"