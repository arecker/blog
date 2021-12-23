'''
render a blog page
'''

import itertools
import logging
import pathlib
import sys

from blog.models import Site

logger = logging.getLogger(__name__)


def main(args):
    site = Site(**vars(args))
    target = site.directory / pathlib.Path(args.page)

    for page in itertools.chain(site.entries, site.pages):
        if page.source == target:
            logger.info('rendering %s', target)
            site.expander.populate()
            print(page.render())
            return

    logger.error('could not find page %s!', target)
    sys.exit(1)


def register(parser):
    parser.add_argument('page', type=str, help='path to page or entry')
