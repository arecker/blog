import configparser
import logging

logger = logging.getLogger(__name__)


def load_config(path: str):
    parser = configparser.ConfigParser()
    parser.read(path)
    logger.debug('loaded config file from %s', path)
    return parser
