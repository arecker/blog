'''
build the website locally
'''

import itertools
import logging
import os

import src as blog

logger = logging.getLogger(__name__)


def main(config, context):
    pave_webroot(context)
    run_build(config, context)


def pave_webroot(context):
    old_files = itertools.chain(context.root_directory.glob('www/*.html'),
                                context.root_directory.glob('www/*.xml'))
    for file in old_files:
        os.remove(file)
        logger.debug('deleting %s', file)


def run_build(config, context):
    blog.build_feeds(config=config, context=context)

    for page in context.pages:
        page.build(context=context, config=config)
        logger.info('rendered %s', page.filename)

    for i, page in enumerate(context.entries):
        page.build(config=config, context=context)
        logger.debug('rendered %s to %s', page, page.target)

        # Log an update every 100 entries and at the end of the list
        if (i + 1) % 100 == 0 or (i + 1) == len(context.entries):
            logger.info('rendered %d out of %d entries', i + 1,
                        len(context.entries))
