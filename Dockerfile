FROM debian:jessie
MAINTAINER Alex Recker

RUN apt-get update && apt-get install -y \
    python python-pip python-dev python-imaging \
    zlib1g zlib1g-dev libpq-dev libjpeg-dev \
    postgresql-client python-psycopg2 \
    gcc supervisor redis-server

RUN mkdir -p /srv
ADD requirements /srv/requirements
RUN pip install -r /srv/requirements/prod.txt
RUN mkdir -p /srv/logs
RUN mkdir -p /srv/src
ADD . /srv/src
RUN find /srv/src -name "*.pyc" -exec rm -rf {} \;
RUN rm -r /srv/src/temp
RUN mkdir -p /srv/static

VOLUME ["/srv/logs/", "/srv/static/"]
EXPOSE 8000
ENTRYPOINT ["/srv/src/docker.sh"]
