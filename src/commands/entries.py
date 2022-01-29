"""build journal entries"""

import logging

from .pages import Page, build_nav_list

logger = logging.getLogger(__name__)


def register(parser):
    return parser


def main(args):
    # TODO: remove once Site is gone
    from ..models import Site
    site = Site(**vars(args))

    total = len(list(site.entries))
    nav_pages = build_nav_list()
    for i, page in enumerate(site.entries):
        page.build(author=args.author,
                   year=args.year,
                   full_url=args.full_url,
                   nav_pages=nav_pages)
        logger.debug('generated %s (%d/%d)', page.target, i + 1, total)
        if (i + 1) % 100 == 0 or (i + 1) == total:
            logger.info('generated %d out of %d entries', i + 1, total)
