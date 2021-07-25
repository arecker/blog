import configparser
import logging

logger = logging.getLogger(__name__)


def load_config(path):
    parser = configparser.ConfigParser()
    parser.read(str(path))
    logger.debug('loaded config file from %s', path)
    return parser
