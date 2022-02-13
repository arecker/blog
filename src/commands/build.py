"""build the website locally"""

import logging

from ..commands import pave, sitemap, feed, index, archives, entries, pets, contact
from .. import utils

logger = logging.getLogger(__name__)


def register(parser):
    return parser


def main(args, nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    pave.main(args)
    index.main(args, nav=nav)
    contact.main(args, nav=nav)
    pets.main(args, nav=nav)
    entries.main(args)
    archives.main(args)
    feed.main(args)
    sitemap.main(args)
