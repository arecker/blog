import collections
import datetime
import functools
import pathlib
import re


class Page:
    """
    A website page.  Can be either a normal page, or a journal entry.
    """

    def __init__(self, path: pathlib.Path, next_page=None, previous_page=None):
        """
        `path` should be a pathlib Path.
        """

        self.path = pathlib.Path(path)

        self._next = next_page
        self._previous = previous_page

    @property
    def filename(self):
        """
        Page filename, e.g. `index.html`.

        The file extension will always be `.html`, so even if the
        source page is rendered from a template, this suffix will be
        removed.
        """
        if self.path.suffix == '.j2':
            return self.path.name[:-3]
        return self.path.name

    @property
    def is_entry(self) -> bool:
        """
        `True` if the page is a journal entry, False if it's just a
        normal Page.
        """
        entry_dir = pathlib.Path('./entries')
        return entry_dir in self.path.parents

    @property
    def date(self) -> datetime.datetime:
        """
        Page date, as parsed from the filename.
        """
        return datetime.datetime.strptime(self.path.stem, '%Y-%m-%d')

    @functools.cached_property
    def metadata(self) -> dict:
        """
        Metadata embedded in the page.  This is read from special HTML
        comments.

        A page with this header:

        ```html
        <!-- meta:title a walk in the park -->
        <!-- meta:description I take a nice walk in the park -->
        ```

        Will yield this metadata:

        ```python
        {
            'title': 'a walk in the park',
            'description': 'I take a nice walk in the park.',
        }
        ```

        For performance, this information is only read once, then
        cached in memory during website build.
        """
        with self.path.open('r') as f:
            return parse_metadata(f.read())

    @property
    def title(self):
        if self.is_entry:
            return self.date.strftime('%A, %B %-d %Y')
        else:
            return self.get('title')

    @property
    def description(self):
        if self.is_entry:
            return self.metadata['title'].replace("'", '')
        else:
            return self.metadata.get('description')

    @property
    def banner(self):
        return self.metadata.get('banner')

    @property
    def next(self):
        """Next `Page` object, if paginated."""
        return self._next

    @property
    def previous(self):
        """Previous `Page` object, if paginated."""
        return self._previous


def load_pages(pages_dir='./pages') -> list[Page]:
    """
    Fetches a list of website pages as `Page` objects.
    """

    pages = pathlib.Path(pages_dir).glob('*.*')
    pages = map(Page, pages)
    return sorted(pages, key=lambda p: p.filename)


def load_entries(entries_dir='./entries') -> list[Page]:
    """
    Fetches a list of journal entries as `Page` objects.

    The list is sorted in descending date, so the latest entry is always
    first.
    """

    entries = []

    entry_paths = list(sorted(pathlib.Path(entries_dir).glob('*.html')))

    # get pagination map
    pagination = paginate_entries(entry_paths)

    for path in entry_paths:
        entries.append(Page(
            path,
            next_page=pagination[path.name].next,
            previous_page=pagination[path.name].previous
        ))

    # sort latest first
    return sorted(entries, reverse=True, key=lambda e: e.date)


Pagination = collections.namedtuple('Pagination', ['next', 'previous'])


def paginate_entries(files=[]) -> Pagination:
    pagination = {}

    for i, this_file in enumerate(files):
        kwargs = {}

        if i > 0:
            kwargs['previous'] = files[i - 1].name
        else:
            kwargs['previous'] = None

        try:
            kwargs['next'] = files[i + 1].name
        except IndexError:
            kwargs['next'] = None

        pagination[this_file.name] = Pagination(**kwargs)

    return pagination


def parse_metadata(content: str) -> dict:
    metadata = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    metadata = [(k, v) for k, v in metadata.findall(content)]
    metadata = dict([(k.strip(), v.strip()) for k, v in metadata])
    return metadata
