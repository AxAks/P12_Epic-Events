# P12_Epic-Events




[comment]: <> (à completer, et penser à faire un script epic_install.sh à la guigui pour lancer tout ca en une ligne !)
Virtualenv (create and activate)
python3.9 -m virtualenv venv
source venv/bin/activate


Create and setup Postgresql database Manually via terminal:

$ sudo su postgres       
$ createdb epiceventsdb
$ psql

postgres=# create user django with password 'djangepic';      
postgres=# grant all privileges on database epiceventsdb to django;        


( python manage.py makemigrations)