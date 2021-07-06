import configparser
import functools

from .files import join
from .logger import logger as l


path = join('blog.conf')
parser = None


def cache_config(func):
    global parser

    @functools.wraps(func)
    def wrapper(*args):
        global parser

        if parser is None:
            l.info('loading program config from %s', path)
            parser = configparser.ConfigParser()
            parser.read(path)

        return func(*args)

    return wrapper


@cache_config
def config(section_name=''):
    try:
        data = dict(parser.items(section_name, {}))
        if not data:
            raise ValueError
        return data
    except (configparser.NoSectionError, ValueError):
        l.warn('config - no data found for section_name %s', section)
        return {}
