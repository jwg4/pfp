#!/bin/bash

#useradd pi?

apt-get install quantlib-python nginx python-django uwsgi uwsgi-plugin-python

service nginx start
service uwsgi start

cd /home/pi/pfp
django-admin startproject pyprice
cd pyprice 
# Do the changes to settings first
./manage.py startproject pyprice
./manage.py startapp yc
./manage.py syncdb
