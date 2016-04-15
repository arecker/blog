#!/bin/bash
cd /srv/src
python manage.py migrate --settings=blog.settings.prod
python manage.py collectstatic --noinput --settings=blog.settings.prod

# exec gunicorn blog.wsgi -b 0.0.0.0:8000 \
#      --log-file /srv/logs/blog.log \
#      --workers 3

exec supervisord -c /srv/src/configs/supervisord.conf
