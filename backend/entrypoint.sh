#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py preload_reference

if [ "$DJANGO_ENV" = "production" ]; then
  echo "running in $DJANGO_ENV mode"
  gunicorn nucleotide_query.wsgi:application --bind 0.0.0.0:8000
else
  echo "running in non production mode"
  python manage.py runserver 0.0.0.0:8000
fi