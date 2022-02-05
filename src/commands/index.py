"""generate the site homepage"""

import logging

from .. import Document

logger = logging.getLogger(__name__)


def main(args):
    document = Document(
        filename='index.html',
        title=args.title,
        description=args.subtitle,
        author=args.author,
        nav_pages=['entries.html', 'pets.html', 'contact.html'],
    )

    with open(document.target, 'w') as f:
        f.write(document.render())
    logger.info('generated %s', document.filename)
