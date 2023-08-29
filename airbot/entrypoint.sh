#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput

exec uvicorn project.asgi:application --host 0.0.0.0