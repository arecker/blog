import datetime
import os
import pathlib


class Page:
    def __init__(self, source, metadata={}):
        self.source = pathlib.Path(source)

        self._metadata = metadata

    @property
    def is_entry(self) -> bool:
        """Returns True if the source file is an entry.

        >>> Page('entries/test.md').is_entry
        True
        """
        return self.source.parent.name == 'entries'

    @property
    def is_markdown(self) -> bool:
        """Returns True if the source file is markdown.

        >>> Page('test.html').is_markdown
        False
        >>> Page('test.md').is_markdown
        True
        """
        _, ext = os.path.splitext(self.source)
        return ext == '.md'

    @property
    def filename(self):
        """Filename of the rendered page target.

        >>> Page('pages/test.html').filename
        'test.html'
        >>> Page('something/something.md').filename
        'something.html'
        """

        basename = os.path.basename(self.source)
        name, _ = os.path.splitext(basename)
        return name + '.html'

    @property
    def metadata(self):
        """Page metadata.

        If the page is markdown, this is extracted from page frontmatter.
        """
        if self._metadata:
            return self._metadata

    @property
    def title(self):
        """Page title.

        If the page is an entry, this will be based on the date.

        >>> Page('entries/2020-01-01.html').title
        'Wednesday, January 1 2020'

        Otherwise, the title is extracted from the metadata field
        "title".

        >>> Page('index.html', {'title': 'Home'}).title
        'Home'
        """
        if not self.is_entry:
            return self.metadata['title']

        return self.date.strftime('%A, %B %-d %Y')

    @property
    def date(self) -> datetime.datetime:
        """Returns the entry date based on the filename.

        >>> Page('entries/2020-01-01.html').date
        datetime.datetime(2020, 1, 1, 0, 0)

        Returns None if not an entry.

        >>> Page('test.html').date is None
        True
        """
        if not self.is_entry:
            return None

        slug, _ = os.path.splitext(self.filename)
        return datetime.datetime.strptime(slug, '%Y-%m-%d')

    def render(self, context: dict):
        """Render a page as an HTML string."""

        return ''
