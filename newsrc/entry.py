import datetime
import glob

from newsrc import partials
from newsrc.files import join
from newsrc.logger import logger
from newsrc.page import Page


def paginate_entries(entries=[]):
    logger.info('building pagination for %d entries', len(entries))

    for i, entry in enumerate(entries):
        if i != 0:
            entry.previous_page = entries[i - 1].permalink

        try:
            entry.next_page = entries[i + 1].permalink
        except IndexError:
            pass


def files():
    return list(reversed(sorted(glob.glob(join('entries/*.*')))))


class Entry(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.next_page = None
        self.previous_page = None

    @property
    def title(self):
        date = datetime.datetime.strptime(self.permalink, '%Y-%m-%d.html')
        return date.strftime('%A %B %-d, %Y')

    @property
    def description(self):
        return self.metadata['title']

    def render_pagination(self):
        return partials.pagination(next_page=self.next_page,
                                   previous_page=self.previous_page)


def entries():
    all_of_them = list(map(Entry, files()))
    paginate_entries(all_of_them)
    return all_of_them
