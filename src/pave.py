"""delete all generated files in webroot"""

import logging
import os

logger = logging.getLogger(__name__)


def main(args):
    targets = list(args.directory.glob('www/*.html'))
    targets += list(args.directory.glob('www/*.xml'))
    for target in targets:
        os.remove(target)
        logger.debug('removed old target %s', target)
    logger.info('paved webroot (%d files)', len(targets))
