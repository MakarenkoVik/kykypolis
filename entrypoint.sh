#!/bin/bash

pip install --upgrade pip
pip install -r requirements.txt

service postgresql status

python manage.py makemigrations
python manage.py migrate

cd service
django-admin makemessages -l ru
django-admin makemessages -l en
django-admin compilemessages
cd ../users
django-admin makemessages -l ru
django-admin makemessages -l en
django-admin compilemessages
cd ..

ls -l

python manage.py runserver
