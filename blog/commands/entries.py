"""build journal entries"""

import logging

from blog.models import Site

logger = logging.getLogger(__name__)


def register(parser):
    return parser


def main(args):
    site = Site(**vars(args))
    total = len(list(site.entries))
    for i, page in enumerate(site.entries):
        page.build(author=args.author, year=args.year, full_url=args.full_url)
        logger.debug('generated %s (%d/%d)', page.target, i + 1, total)
        if (i + 1) % 100 == 0 or (i + 1) == total:
            logger.info('generated %d out of %d entries', i + 1, total)
