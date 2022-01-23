"""delete all generated files in webroot"""

import logging
import os
import pathlib

logger = logging.getLogger(__name__)
root_dir = pathlib.Path(__file__).parent.parent.parent


def main(args):
    targets = list(root_dir.glob('www/*.html'))
    for target in targets:
        os.remove(target)
        logger.debug('removed old target %s', target)
    logger.info('paved webroot (%d files)', len(targets))
