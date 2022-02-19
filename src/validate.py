"""validate site files"""

import logging

logger = logging.getLogger(__name__)

def main(args):
    pages = sorted(list(args.directory.glob('www/*.html')))
    assert pages, 'No pages found!  Build the project first.'
