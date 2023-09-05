#!/bin/bash

<<<<<<< HEAD
python manage.py migrate && python manage.py collectstatic --noinput && python manage.py createsuperuser --noinput

=======
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput
>>>>>>> 3bec8d3025f44fe31df7c51d511cc2c2f2024e3b
exec uvicorn airbot.asgi:application --host 0.0.0.0