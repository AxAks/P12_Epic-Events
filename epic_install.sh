#!/bin/bash

current_user=$(whoami)

echo "Epic Events Installation."
echo "The environment and requirements will now be installed..."
python3.9 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation of the Epic Events Database..."
echo "This requires root actions. Please enter your password when asked"
sudo su postgres <<EOF
service postgresql restart
psql -c 'DROP DATABASE epicdb;'
psql -c 'CREATE DATABASE epicdb;'
psql -c "DROP USER epicuser;"
psql -c "CREATE USER epicuser WITH PASSWORD 'djangepic';"
psql -c 'GRANT ALL PRIVILEGES on DATABASE epicdb to epicuser;'
EOF

sudo su "${$current_user}"

source venv/bin/activate
cd epic_events/

echo "deleting previous migrations in case of re-installation..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "creating database tables models..."
python manage.py makemigrations
echo "creating tables in database..."
python manage.py migrate
echo "inserting default data..."
python manage.py loaddata core/fixtures/departments_fixtures.json

echo "Epic Events Installation successfully completed !"
