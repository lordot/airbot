#!/bin/bash

./manage.py collectstatic --noinput

./manage.py migrate
./manage.py createsuperuser --no-input

exec uvicorn airbot.asgi:application --host 0.0.0.0