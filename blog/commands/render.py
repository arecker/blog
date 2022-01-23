'''
render a blog page
'''

import itertools
import logging
import pathlib
import pathlib
import sys

from blog.models import Site

logger = logging.getLogger(__name__)
root_dir = pathlib.Path(__file__).parent.parent.parent


def main(args):
    site = Site(**vars(args))
    target = root_dir / pathlib.Path(args.page)

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
