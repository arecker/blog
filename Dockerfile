FROM debian:jessie
MAINTAINER Alex Recker

RUN apt-get update && apt-get install -y \
    python python-pip python-dev python-imaging \
    zlib1g zlib1g-dev libpq-dev libjpeg-dev \
    postgresql-client python-psycopg2 \
    gcc

RUN mkdir -p /srv/src
COPY . /srv/src

RUN mkdir -p /srv/logs
RUN touch /srv/logs/blog.log

VOLUME [/srv/logs/]

WORKDIR /srv/src
RUN pip install -r requirements/prod.txt

EXPOSE 8000

ENTRYPOINT /srv/src/docker.sh
