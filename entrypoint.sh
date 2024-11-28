#!/bin/sh

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 0.5
done
sleep 2
echo "Redis is up!"

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

celery -A ProZdorovye worker -l info -P prefork &
celery -A ProZdorovye flower -l info &
gunicorn ProZdorovye.wsgi:application --bind 0.0.0.0:8000 &

wait