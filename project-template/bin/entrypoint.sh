#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.5
done

echo "PostgreSQL started"

cd src
# python manage.py flush --no-input
python manage.py migrate

exec "$@"