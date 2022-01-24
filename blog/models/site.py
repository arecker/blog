import datetime
import functools
import logging
import os
import pathlib

from blog import macro, git, utils
from blog.models.page import Page

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent
root_dir = here.parent.parent


class Site:
    def __init__(self, **kwargs):
        self.basepath = kwargs.pop('basepath', '/')
        self.timestamp = kwargs.pop('timestamp', datetime.datetime.now())

        self._pages = kwargs.pop('pages', None)
        self._entries = kwargs.pop('entries', None)

    def __repr__(self):
        return f'<Site {utils.prettify_path(root_dir)}>'

    @property
    def entries(self):
        if not self._entries:
            sources = sorted(root_dir.glob('entries/*.html'), reverse=True)
            self._entries = [
                Page(source=source, site=self) for source in sources
            ]

        return self._entries

    @property
    def pages(self):
        if not self._pages:
            sources = sorted(root_dir.glob('pages/*.html'))
            self._pages = [
                Page(source=source, site=self) for source in sources
            ]

        return self._pages

    @functools.cached_property
    def nav(self):
        pages = sorted(filter(lambda p: p.nav_index, self.pages),
                       key=lambda p: p.nav_index)
        return ['entries.html'] + [p.filename for p in pages]

    @property
    def latest(self):
        return self.entries[0]

    @functools.cached_property
    def expander(self):
        e = macro.Expander(site=self)
        e.populate()
        return e

    @functools.cached_property
    def pagination(self):
        filenames = [f.filename for f in reversed(self.entries)]
        return utils.paginate_list(filenames)

    @functools.cached_property
    def commit(self):
        return git.get_head_commit(root_dir)

    @functools.cached_property
    def is_entry_tagged(self):
        return git.head_is_entry_tagged(root_directory=root_dir)
