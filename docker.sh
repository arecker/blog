#!/bin/bash
cd /srv/src
python manage.py migrate --settings=blog.settings.prod
python manage.py collectstatic --noinput --settings=blog.settings.prod
exec supervisord -c /srv/src/configs/supervisord.conf
