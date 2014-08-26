#!/bin/bash

#useradd pi?

apt-get install quantlib-python nginx python-django uwsgi uwsgi-plugin-python

service nginx start

cd /home/pi/pfp
django-admin startproject pyprice
cd pyprice 
# Do the changes to settings first
./manage.py syncdb

service uwsgi start
