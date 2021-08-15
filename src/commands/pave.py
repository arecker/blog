'''
delete all generated files in webroot
'''

import logging

import src as blog

logger = logging.getLogger(__name__)


def main(args):
    site = blog.Site(args)
    site.pave()
    logger.info('paved webroot!')
