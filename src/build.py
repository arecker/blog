"""Build the website locally"""

import blog
import logging

from . import pave, feed, index, entries as entriescmd

logger = logging.getLogger(__name__)


def main(args, entries=[]):
    entries = entries or blog.all_entries(args.directory / 'entries')

    pave.main(args)
    index.main(args)
    entriescmd.main(args, entries=entries)
    feed.main(args, entries=entries)

    blog.write_sitemap(args.directory / 'www',
                       full_url=args.full_url,
                       entries=entries)
