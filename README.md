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
Download the project:      
in the terminal:          
$ git clone https://github.com/AxAks/P12_Epic-Events.git


* using the installation script:       
$ cd P12_Epic-Events/
Launch installation script:          
$ ./epic_install.sh (or $ sh ./epic_install.sh)    
-> and follow the instructions

******

* In case the script does not work:    
$ cd P12_Epic-Events/    
Create and activate the Virtual environment:    
$ python3.9 -m virtualenv venv   
$ source venv/bin/activate   
$ pip install -r requirements.txt    
Handle environment variables with dotenv:   
$ touch .env    

open the .env file set the following values:   
SECRET_KEY = 'example'   
DB_NAME = 'example'   
DB_USER ='example'   
DB_PASSWORD = 'example'   
DB_HOST = 'example'  (localhost as default)   
DB_PORT = 'example'  (5432 as default)   
PATH_TO_LOGS = 'example.log'   

touch epic_events/example.log    

Create and setup Postgresql database Manually:    
$ sudo su postgres       
$ sudo service postgresql restart     
$ createdb [DB_NAME]    
$ psql    
postgres=# create user [DB_USER] with password '[DB_PASSWORD]';       
postgres=# grant all privileges on database [DB_NAME] to [DB_USER];
sudo su [CURRENT_USER]   
source venv/bin/activate   
cd epic_events/
python manage.py makemigrations    
python manage.py migrate   
python manage.py loaddata core/fixture/departments_fixtures.json    

Create The Application SuperUser:    
python manage.py createsuperuser    




## 4. Execution <a name="execution"></a>
Activate the virtual environment:     
$ source venv/bin/activate 

Change to the right directory:       
$ cd epic_events    

Launch the server with:      
$ python manage.py runserver    


## 5. Usage <a name="usage"></a>

Administration Site:
Access to the administration site as SuperUser or via a Manager profile at http://localhost:8000/admin/    
- the first Manager profile must be created by the SuperUser
- A Manager can create accounts for all employees (other managers, sales team, or support team)
- Deletions are enabled on the administration interface only 

API:
Documentation of The API at https://documenter.getpostman.com/view/12451273/UyxqBi5W    

Profile Right:
SuperUser:
- All Rights granted (including deletions)

Manager:
- Management of Employees (Creation, Access, Update) 
- Updates on any Model (Client, Contract, Event) 
- Assignments (follow-up details on Client, Contracts, Events): Creation and Deletion (as an update of the information)

Sales:
- Access to Clients, Contracts, Events (Creation, View, Update, Assignation)

Support:
- Viewing Access to clients and contracts information limited to the events they are assigned to
- Access to the events they are assigned to (view and update)