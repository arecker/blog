FROM nginx
MAINTAINER Alex Recker <alex@reckerfamily.com>

COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN echo "<title>Blog by Alex Recker</title>" > /usr/share/nginx/html/index.html
