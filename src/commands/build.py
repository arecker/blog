"""build the website locally"""

import logging

from ..commands import pave, sitemap, feed, index, archives, entries, pages

logger = logging.getLogger(__name__)


def register(parser):
    feed.register(parser)
    entries.register(parser)
    pages.register(parser)
    index.register(parser)


def main(args):
    pave.main(args)
    index.main(args)
    pages.main(args)
    entries.main(args)
    archives.main(args)
    feed.main(args)
    sitemap.main(args)
