import logging
import os
import platform
import sys

from . import files


logger = logging.getLogger(__name__)


def configure_logger(_logger):
    log_level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO').upper())
    _logger.setLevel(log_level)
    _logger.handlers = []
    _logger.addHandler(logging.StreamHandler(sys.stdout))


def main():
    configure_logger(logger)
    logger.debug('starting blog, python = %s', platform.python_version())
