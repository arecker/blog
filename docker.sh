#!/bin/bash
cd /srv/src

echo "In docker.sh" >> /srv/logs/blog.log
echo "DB_USER: $DB_USER" >> /srv/logs/blog.log
echo "DB_PASS: $DB_PASS" >> /srv/logs/blog.log
echo "PWD: $(pwd)" >> /srv/logs/blog.log

python manage.py migrate --settings=blog.settings.prod
python manage.py collectstatic --noinput --settings=blog.settings.prod

exec gunicorn blog.wsgi -b 0.0.0.0:8000 \
     --log-file /srv/logs/blog.log \
     --workers 3
