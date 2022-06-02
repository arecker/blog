import collections
import json
import logging
import pathlib

logger = logging.getLogger(__name__)

Redirect = collections.namedtuple('Redirects', ['source', 'target'])


def write_redirects(www_dir='', data_dir=''):
    redirects = []
    with (pathlib.Path(data_dir) / 'redirects.json').open('r') as f:
        for (source, target) in json.load(f):
            redirects.append(Redirect(source=source, target=target))

    with (pathlib.Path(www_dir) / '_redirects').open('w') as f:
        for redirect in sorted(redirects, key=lambda r: r.source):
            f.write(f'{redirect.source} {redirect.target}\n')
    logger.info('rendered %d redirect(s) to www/_redirects', len(redirects))
