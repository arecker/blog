'''
render a blog page
'''

import itertools
import logging
import pathlib
import sys

from ..models import Site
from ..utils import ROOT_DIR

logger = logging.getLogger(__name__)


def main(args):
    site = Site(**vars(args))
    target = ROOT_DIR / pathlib.Path(args.page)

    for page in itertools.chain(site.entries, site.pages):
        if page.source == target:
            logger.info('rendering %s', target)
            site.expander.populate()
            print(page.render(author=args.author))
            return

    logger.error('could not find page %s!', target)
    sys.exit(1)


def register(parser):
    parser.add_argument('page', type=str, help='path to page or entry')
