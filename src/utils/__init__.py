"""Package for random functions."""
from .string_writer import StringWriter

import blog
import collections
import datetime
import logging
import typing
import urllib.parse

logger = logging.getLogger(__name__)


def to_iso_date(date):
    return date.replace(tzinfo=datetime.timezone.utc).isoformat()


Page = collections.namedtuple(
    'Page',
    [
        'filename',
        'title',
        'description',
        'banner',
        'page_next',
        'page_previous',
    ],
)
