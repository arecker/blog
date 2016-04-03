from uuid import uuid4

from django.db import models
from django.conf import settings
from pyshorteners import Shortener


def get_uuid_pk():
    return models.UUIDField(primary_key=True,
                            default=uuid4,
                            editable=False,
                            unique=True)


def to_full_url(relative_url=''):
    return '{}{}'.format(settings.URL_BASE, relative_url)


def shorten_url(long_url=''):
    return Shortener('Tinyurl').short(long_url)
