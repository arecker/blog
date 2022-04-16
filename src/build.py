"""Build the website locally"""

import blog
import logging

from . import pave, sitemap, feed, index, entries as entriescmd, utils

logger = logging.getLogger(__name__)


def main(args, entries=[]):
    entries = entries or blog.all_entries(args.directory)

    pave.main(args)
    index.main(args)
    entriescmd.main(args, entries=entries)
    feed.main(args, entries=entries)
    sitemap.main(args, entries=entries)
