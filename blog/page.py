import datetime
import os
import pathlib
from xml.etree import ElementTree


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
    def description(self):
        """The page description.

        If the page is an entry, this will map to the 'title' metadata
        field.

        >>> Page('entries/test.html', {'title': 'my big dumb mouth'}).description
        'my big dumb mouth'

        Otherwise, this will map to the 'description' metadata field.

        >>> Page('index.html', {'description': 'The Index'}).description
        'The Index'
        """
        if self.is_entry:
            return self.metadata['title']
        return self.metadata['description']

    @property
    def date(self) -> datetime.datetime:
        """Entry date based on the filename.

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

    def html_header(self):
        """Renders the HTML page header, based on the page title and
        description.

        >>> metadata = {'title': 'One Fat Summer', 'description': 'A Book Report'}
        >>> element = Page('page.html', metadata).html_header()
        >>> ElementTree.indent(element)
        >>> ElementTree.dump(element)
        <header>
          <h1>One Fat Summer</h1>
          <h1>A Book Report</h1>
        </header>
        """

        tree = ElementTree.TreeBuilder()
        tree.start('header', {})
        tree.start('h1', {})
        tree.data(self.title)
        tree.end('h1')
        tree.start('h1', {})
        tree.data(self.description)
        tree.end('h1')
        tree.end('header')
        return tree.close()

    def render(self, context: dict):
        """Render a page as an HTML string."""

        return ''
