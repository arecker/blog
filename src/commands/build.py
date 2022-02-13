"""build the website locally"""

import logging

from ..commands import pave, sitemap, feed, index, archives, entries as entriescmd, pets, contact
from .. import utils

logger = logging.getLogger(__name__)


def register(parser):
    return parser


def main(args, nav=[], entries=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    entries = entries or utils.fetch_entries(args.directory / 'entries')
    pave.main(args)
    index.main(args, nav=nav)
    contact.main(args, nav=nav)
    pets.main(args, nav=nav)
    entriescmd.main(args, nav=nav, entries=entries)
    archives.main(args)
    feed.main(args, entries=entries)
    sitemap.main(args)
