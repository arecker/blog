FROM debian:latest
MAINTAINER Alex Recker <alex@reckerfamily.com>
RUN apt-get update && apt-get install -y emacs python python-pip
RUN pip install awscli
RUN useradd --create-home -s /bin/bash blog
WORKDIR /home/blog
USER blog
