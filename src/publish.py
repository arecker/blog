import argparse
import logging
import re

from . import lib

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument('--dir-entries', required=True)


def main():
    args = parser.parse_args()

    lib.git_add('.')
    logger.info('staged files')

    latest = lib.fetch_entries(args.dir_entries)[0]
    message = 'entry: ' + latest.title
    lib.git_commit(message)
    logger.info('created new commit "%s"', message)

    tag = 'entry-' + re.sub(r'.html$', '', latest.filename)
    lib.git_tag(tag)
    logger.info('created new tag "%s"', tag)

    lib.git_push_tags()
    logger.info('pushed tag %s', tag)

    lib.git_push_branch('master')
    logger.info('pushed branch')

    logger.info('latest entry "%s" published', latest.description)


if __name__ == '__main__':
    lib.configure_logging()
    main()
