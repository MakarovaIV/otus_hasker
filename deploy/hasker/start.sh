#!/bin/bash

set -e

sleep 5

echo "${0}: running migrations."
python3 /app/hasker/hasker/manage.py makemigrations
python3 /app/hasker/hasker/manage.py migrate

echo "${0}: starting app."
python3 /app/hasker/hasker/manage.py runserver 0.0.0.0:80
