FROM nginx
MAINTAINER Alex Recker <alex@reckerfamily.com>

COPY nginx.conf /etc/nginx/conf.d/default.conf
