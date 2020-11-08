import logging
import sys

from . import git, images


logger = logging.getLogger('blog')


def main():
    if not images.imagemagick_installed():
        logger.warning(
            '`convert` command not available in path, skipping image resize!'
        )
        sys.exit(0)

    for new_file in filter(images.is_image, git.new_files()):
        logger.debug('checking size of %s', new_file)
        if images.is_too_big(new_file):
            logger.info('%s is too big, resizing...', new_file)
            images.resize(new_file)
            logger.debug('staging %s', new_file)
            git.stage(new_file)
        else:
            logger.debug('%s is already small enough, skipping...', new_file)


if __name__ == '__main__':
    from .logging import configure_logging
    configure_logging()
    main()
