#!/bin/bash

python manage.py collectstatic --noinput

python manage.py migrate
python manage.py createsuperuser --no-input

exec uvicorn airbot.asgi:application --host 0.0.0.0