import collections


Site = collections.namedtuple('Site', [
    'protocol',
    'domain',
    'timestamp',
    'author',
])


from .template import render_template, render_page
from .entry import load_entries
from .page import load_pages
