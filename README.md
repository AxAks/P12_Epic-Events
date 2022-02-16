# P12_Epic-Events




python3.9 -m virtualenv venv


$ createdb epiceventsdb


sudo su postgres
postgres=# create user django with password 'djangepic';
postgres=# create database epiceventsdb;
postgres=# grant all privileges on database epiceventsdb to django;

