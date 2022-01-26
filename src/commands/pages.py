"""build website pages"""

import logging

from ..utils import ROOT_DIR
from ..pages import Page, build_nav_list
from ..models import Site

logger = logging.getLogger(__name__)


def register(parser):
    return parser


def main(args):
    pages = sorted(ROOT_DIR.glob('pages/*.html'))

    # TODO: remove once macro library is gone
    site = Site(**vars(args))

    pages = [Page(source=source, site=site) for source in pages]
    nav_pages = build_nav_list()
    total = len(pages)
    for i, page in enumerate(pages):
        page.build(author=args.author,
                   year=args.year,
                   full_url=args.full_url,
                   nav_pages=nav_pages)
        logger.info('generated %s (%d/%d pages)', page.target, i + 1, total)
