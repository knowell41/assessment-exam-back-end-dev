#!/bin/bash
python manage.py collectstatic --no-input
python manage.py migrate

if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --no-input \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL"
fi

export WORKERS=${SERVER_WORKERS:-3}
export TIMEOUT=${WORKER_TIMEOUT:-180}
exec gunicorn server.wsgi --workers=$WORKERS --timeout $TIMEOUT --bind 0.0.0.0:8000 --access-logfile -
