import logging

from . import images


logger = logging.getLogger('blog')


def main():
    files = images.files()
    logger.info('scanning %d image(s)', len(files))
    for file in files:
        if images.is_too_big(file):
            logger.info('resizing %s', file)
            images.resize(file)
        else:
            logger.debug('%s is the correct size, skipping...', file)
    logger.info('image size scan complete')


if __name__ == '__main__':
    from .logging import configure_logging
    configure_logging()
    main()
