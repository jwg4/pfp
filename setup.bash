#!/bin/bash

#useradd pi?

apt-get install quantlib-python nginx python-django

service nginx start

cd /home/pi/pfp
django-admin startproject pyprice
cd pyprice 
# Do the changes to settings first
./manage.py syncdb
# This is only for testing - remove it when we have details of
# how to setup the prod server
./manage.py runserver 192.168.0.6:8000

