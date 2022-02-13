"""build the website locally"""

import logging

from ..commands import pave, sitemap, feed, index, archives, entries, pages, pets
from .. import utils

logger = logging.getLogger(__name__)


def register(parser):
    feed.register(parser)
    entries.register(parser)
    pages.register(parser)
    index.register(parser)


def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    pave.main(args)
    index.main(args)
    pages.main(args)
    pets.main(args, nav=nav)
    entries.main(args)
    archives.main(args)
    feed.main(args)
    sitemap.main(args)
