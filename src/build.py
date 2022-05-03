"""Build the website locally"""

import blog
import logging

from . import pave, index, entries as entriescmd

logger = logging.getLogger(__name__)


def main(args, entries=[]):
    entries = entries or blog.all_entries(args.directory / 'entries')

    pave.main(args)
    index.main(args)
    entriescmd.main(args, entries=entries)

    blog.write_feed(args.directory / 'www',
                    title=args.title,
                    subtitle=args.subtitle,
                    author_name=args.author,
                    author_email=args.email,
                    timestamp=entries[0].date,
                    full_url=args.full_url.geturl(),
                    entries=entries[0:50])

    blog.write_sitemap(args.directory / 'www',
                       full_url=args.full_url,
                       entries=entries)
