import collections
import configparser
import logging
import re

logger = logging.getLogger(__name__)


def load_config(path):
    parser = configparser.ConfigParser()
    parser.read(str(path))
    logger.debug('loaded config file from %s', path)
    return parser
