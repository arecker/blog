"""build website pages"""

import logging

from blog.models import Site

logger = logging.getLogger(__name__)


def register(parser):
    return parser


def main(args):
    site = Site(**vars(args))

    total = len(list(site.pages))
    for i, page in enumerate(site.pages):
        page.build(author=args.author, year=args.year, full_url=args.full_url)
        logger.info('generated %s (%d/%d pages)', page.target, i + 1, total)
