#!/bin/bash

pip install --upgrade pip
pip install -r requirements.txt

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

python manage.py runserver
