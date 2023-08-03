#./venv/bin/python
import datetime
import logging
import sys


logger = logging.getLogger(__name__)


def main():
    start = datetime.datetime.now()
    logger.info('program starting')
    duration = datetime.datetime.now() - start
    logger.info('program finished in %ds', duration.seconds)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='build: %(message)s', stream=sys.stderr)
    main()
