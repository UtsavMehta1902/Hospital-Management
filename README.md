# Hospital-Management
This is the repository for the mini course project of Database Management Laboratory CS39202 for the Spring semester 2022-23, at IIT Kharagpur.

## 1. Installation  
1st create python virtual environment and activate it.  
```bash
python3 -m venv env
source env/bin/activate
```
Then install the required packages using the following command
```bash
python3 -m pip install --upgrade pip
python3 -m pip install Django
python3 -m pip install django-widget-tweaks
python3 -m pip install matplotlib
python3 -m pip install xhtml2pdf
```
## 2. Database connection
If you want to use the mysql database, then install the following packages
```bash
python3 -m pip install mysqlclient
python3 -m pip install mysql-connector-python
```
## 3. How to run the code:
```bash
python3 hospitalmanagement-master/manage.py makemigrations hospital
python3 hospitalmanagement-master/manage.py migrate
python3 hospitalmanagement-master/manage.py runserver
```
