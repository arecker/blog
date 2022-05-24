import collections
import json
import logging
import pathlib

logger = logging.getLogger(__name__)

Info = collections.namedtuple('Info', [
    'author',
    'email',
    'subtitle',
    'title',
    'url',
])


def load_info(dir_data) -> Info:
    target = pathlib.Path(dir_data) / 'info.json'
    with open(target, 'r') as f:
        kwargs = json.load(f)
        info = Info(**kwargs)
        logger.info('parsed site info from %s', target)
        return info
