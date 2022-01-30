import datetime
import functools
import logging

from .. import macro, git, utils
from ..models.page import Page

logger = logging.getLogger(__name__)


class Site:
    def __init__(self, **kwargs):
        self._pages = kwargs.pop('pages', None)
        self._entries = kwargs.pop('entries', None)

    def __repr__(self):
        return f'<Site {utils.prettify_path(utils.ROOT_DIR)}>'

    @property
    def entries(self):
        from ..commands.entries import Entry
        if not self._entries:
            sources = sorted(utils.ROOT_DIR.glob('entries/*.html'),
                             reverse=True)
            self._entries = [
                Entry(source=source, site=self) for source in sources
            ]

        filenames = [f.filename for f in reversed(self._entries)]
        pagination = utils.paginate_list(filenames)
        for entry in self._entries:
            pages = pagination[entry.filename]
            entry.paginate(next_filename=pages.next,
                           previous_filename=pages.previous)

        return self._entries

    @property
    def pages(self):
        if not self._pages:
            sources = sorted(utils.ROOT_DIR.glob('pages/*.html'))
            self._pages = [
                Page(source=source, site=self) for source in sources
            ]

        return self._pages

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
