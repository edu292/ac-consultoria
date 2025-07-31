release: python manage.py collectstatic --noinput
web: gunicorn ac_consultoria.wsgi
worker: celery -A ac_consultoria worker -l info -P gevent -c 100