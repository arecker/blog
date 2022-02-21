"""validate site files"""

import logging
import xml.etree.ElementTree

from . import utils

logger = logging.getLogger(__name__)

def main(args):
    for f in ['feed.xml', 'sitemap.xml']:
        target = args.directory / 'www' / f
        xml.etree.ElementTree.parse(target)
        logger.info('validated %s', utils.prettify_path(target))
