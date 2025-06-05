#!/bin/sh

python manage.py preload_reference

if [ "$DJANGO_ENV" = "production" ]; then
  gunicorn project.wsgi:application --bind 0.0.0.0:8000
else
  python manage.py runserver 0.0.0.0:8000
fi