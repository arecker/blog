"""build the website locally"""

import logging

from blog.commands import pave, sitemap, feed, archives
from blog.models import Site

logger = logging.getLogger(__name__)


def register(parser):
    feed.register(parser)


def main(args):
    pave.main(args)
    archives.main(args)
    feed.main(args)
    sitemap.main(args)

    site = Site(**vars(args))

    total = len(list(site.pages))
    for i, page in enumerate(site.pages):
        page.build(author=args.author)
        logger.info('generated %s (%d/%d pages)', page.target, i + 1, total)

    total = len(list(site.entries))
    for i, page in enumerate(site.entries):
        page.build(author=args.author)
        logger.debug('generated %s (%d/%d)', page.target, i + 1, total)
        if (i + 1) % 100 == 0 or (i + 1) == total:
            logger.info('generated %d out of %d entries', i + 1, total)
