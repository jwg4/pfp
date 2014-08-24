#!/bin/bash

#useradd pi?

apt-get install quantlib-python nginx python-django

service nginx start

cd /home/pi/pfp
django-admin startproject pyprice
cd pyprice 
./manage.py syncdb
