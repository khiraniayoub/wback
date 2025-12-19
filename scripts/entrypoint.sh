#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DJANGO_POSTGRESQL_HOST $DJANGO_POSTGRESQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

uv run manage.py migrate --settings=wback.settings
uv run manage.py collectstatic --noinput --settings=wback.settings

exec "$@"
