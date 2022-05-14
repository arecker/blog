import argparse
import logging
import re

from . import git, entries

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument('--dir-entries', required=True)


def main():
    args = parser.parse_args()

    git.git_add('.')
    logger.info('staged files')

    latest = entries.all_entries(args.dir_entries)[0]
    message = 'entry: ' + latest.title
    git.git_commit(message)
    logger.info('created new commit "%s"', message)

    tag = 'entry-' + re.sub(r'.html$', '', latest.filename)
    git.git_tag(tag)
    logger.info('created new tag "$s"', tag)

    git.git_push_tag(tag)
    logger.info('pushed tag %s', tag)

    git.git_push_branch('master')
    logger.info('pushed branch')

    logger.info('latest entry "%s" published', latest.description)


if __name__ == '__main__':
    main()
