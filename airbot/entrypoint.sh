#!/bin/bash

python manage.py migrate && python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput

exec uvicorn airbot.asgi:application --host 0.0.0.0