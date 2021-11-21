"""build the website locally"""

import logging

from src.commands import pave
from src.models import Site

logger = logging.getLogger(__name__)


def main(args):
    site = Site(args)
    site.expander.populate()

    pave.main(args)

    site.feed.build()
    logger.info('generated %s (1/2 feeds)', site.feed.target)
    site.sitemap.build()
    logger.info('generated %s (2/2 feeds)', site.sitemap.target)

    total = len(list(site.pages))
    for i, page in enumerate(site.pages):
        page.build()
        logger.info('generated %s (%d/%d pages)', page.target, i + 1, total)

    total = len(list(site.entries))
    for i, page in enumerate(site.entries):
        page.build()
        logger.debug('generated %s (%d/%d)', page.target, i + 1, total)
        if (i + 1) % 100 == 0 or (i + 1) == total:
            logger.info('generated %d out of %d entries', i + 1, total)
