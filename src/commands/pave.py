"""delete all generated files in webroot"""

import itertools
import logging
import os

import src as blog

logger = logging.getLogger(__name__)


def make_target_list(site):
    chain = itertools.chain(site.entries, site.pages,
                            [site.feed, site.sitemap])
    return [site.directory / thing.target for thing in chain]


def main(args):
    site = blog.Site(args)
    targets = make_target_list(site)

    for target in filter(os.path.exists, targets):
        os.remove(target)
        logger.debug('removed old target %s',
                     target.relative_to(site.directory))

    logger.info('paved webroot (%d files)', len(targets))
