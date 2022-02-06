import copy
import functools
import logging

from .. import utils
from ..models.page import Page

logger = logging.getLogger(__name__)


class Site:
    def __init__(self, **kwargs):
        self._pages = kwargs.pop('pages', None)
        self._entries = kwargs.pop('entries', None)

    def __repr__(self):
        return f'<Site {utils.prettify_path(utils.ROOT_DIR)}>'

    @functools.cached_property
    def entries(self):
        from ..commands.entries import Entry
        if self._entries:
            return self._entries

        entries = sorted(utils.ROOT_DIR.glob('entries/*.html'), reverse=True)

        entries = [Entry(source=source, site=self) for source in entries]

        filenames = [f.filename for f in reversed(entries)]
        pagination = utils.paginate_list(filenames)
        for entry in entries:
            pages = pagination[entry.filename]
            entry.paginate(next_filename=pages.next,
                           previous_filename=pages.previous)
        return entries

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
    def pagination(self):
        filenames = [f.filename for f in reversed(self.entries)]
        return utils.paginate_list(filenames)
