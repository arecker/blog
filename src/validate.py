import collections
import html.parser
import logging
import pathlib

logger = logging.getLogger('blog')


Reference = collections.namedtuple('Reference', [
    'attr',
    'path',
    'value',
])


class ReferenceParser(html.parser.HTMLParser):
    def __init__(self, parent):
        self.parent = pathlib.Path(parent)
        self.references = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            key, val = attr
            val = val or ''
            if key not in ['src', 'href']:
                continue
            if not val.startswith('./'):
                continue
            self.references.append(Reference(
                attr=key,
                value=val,
                path=(self.parent / val)
            ))


def validate_html_references(path: str | pathlib.Path) -> int:
    """Validate an HTML file
    """

    path = pathlib.Path(path)

    with path.open('r') as f:
        content = f.read()

    # check refs
    checker = ReferenceParser(parent=path.parent)
    checker.feed(content)
    for reference in checker.references:
        if not reference.path.is_file():
            logger.warn('%s: %s reference not found: %s',
                        path.name, reference.attr, reference.value)
    return len(checker.references)
