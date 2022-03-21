#!/bin/bash

current_user=$(whoami)

printf "Epic Events Installation.\n"
printf "The environment and requirements will now be installed...\n"
python3.9 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

printf "You will now be asked to provide the needed environment variables\n"
touch epic_events/.env

printf "Please provide a secret key for the Django app: \n"
read SECRET_KEY
printf "\nPlease provide a database name: \n"
read DB_NAME
printf "\nPlease provide a Django username for the PostgreSQL Database: \n"
read DB_USER
printf "\nPlease provide a password for the Django user: \n"
read DB_PASSWORD
printf "\nPlease provide a name for the app logs file: \n"
read PATH_TO_LOGS

printf "SECRET_KEY = '$SECRET_KEY'\n
DB_NAME = '$DB_NAME'\n
DB_USER = '$DB_USER'\n
DB_PASSWORD = '$DB_PASSWORD'\n
PATH_TO_LOGS = '$PATH_TO_LOGS'\n" > epic_events/.env

touch epic_events/$PATH_TO_LOGS


printf "Installation of the Epic Events Database...\n"
printf "This requires root actions. Please enter your password when asked\n"
sudo su postgres <<EOF
service postgresql restart
psql -c 'DROP DATABASE $DB_NAME;'
psql -c 'CREATE DATABASE $DB_NAME;'
psql -c "DROP USER $DB_USER;"
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
psql -c 'GRANT ALL PRIVILEGES on DATABASE $DB_NAME to $DB_USER;'
EOF

sudo su "${$current_user}"

source venv/bin/activate
cd epic_events/

printf "Creating database\n"

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata core/fixtures/departments_fixtures.json

printf "Epic Events Installation successfully completed !\n"
