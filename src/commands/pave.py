"""delete all generated files in webroot"""

import logging
import os

from ..utils import ROOT_DIR

logger = logging.getLogger(__name__)


def main(args):
    targets = list(ROOT_DIR.glob('www/*.html'))
    for target in targets:
        os.remove(target)
        logger.debug('removed old target %s', target)
    logger.info('paved webroot (%d files)', len(targets))
