# flake8: noqa
"""the greatest static HTML journal generator ever made"""
from .introspect import src_dir, fetch_commands
from .utils import StringWriter
from .render import render_index, slugify
