# P12_Epic-Events
Study project : Django-based CRM 

## Chapters

1. [Presentation](#presentation)
2. [Prerequisites (for developers)](#prerequisites)
3. [Installation](#installation)
4. [Execution](#execution)
5. [Usage](#usage)


## 1. Presentation <a name="presentation"></a>

This project provides a Django REST API along with a customized Django Admin Interface.
It will be used as an internal CRM (Customer Relationship Management) software for Epic Events



## 2. Prerequisites (for developers) <a name="prerequisites"></a>
This program runs under python 3.9 in a virtual environment and a postgresql database.
insofar as the followings are installed:
- python 3.9 (including pip3)
- virtualenv
- postgresql 12+


## 3. Installation <a name="installation"></a>



[comment]: <> (à completer, et penser à faire un script epic_install.sh à la guigui pour lancer tout ca en une ligne !)
[comment]: <> git clone https://github.com/AxAks/P12_Epic-Events.git
[comment]: <> cd P12_Epic-Events/
[comment]: <> sh ./epic_install.sh

In case the script does not work:

git clone https://github.com/AxAks/P12_Epic-Events.git
Virtualenv (create and activate)
python3.9 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

Create and setup Postgresql database Manually via terminal:

$ sudo su postgres     
$ sudo service postgresql restart
$ createdb epiceventsdb
$ psql

postgres=# create user django with password 'djangepic';      
postgres=# grant all privileges on database epiceventsdb to django;        


python manage.py makemigrations
python manage.py migrate
python manage.py loaddata core/fixture/departments_fixtures.json


python manage.py runserver

