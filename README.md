# P12_Epic-Events



Virtualenv (create and activate)
python3.9 -m virtualenv venv
source venv/bin/activate

Create and setup Postgresql database Manually via terminal:

$ sudo su postgres       
$ createdb epiceventsdb
$psql

postgres=# create user django with password 'djangepic';     
postgres=# create database epiceventsdb;     
postgres=# grant all privileges on database epiceventsdb to django;        


( python manage.py makemigrations)