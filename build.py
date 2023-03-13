#!./venv/bin/python

import argparse
import collections
import datetime
import io
import logging
import pathlib
import re
import sys

import jinja2


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='store_true')
group.add_argument('-s', '--silent', action='store_true')


Entry = collections.namedtuple('Entry', [
    'filename',
    'title',
    'subtitle',
    'date',
    'banner',
    'content',
    'pages',
])
Pagination = collections.namedtuple('Pagination', ['next', 'previous'])


def load_entries() -> list[Entry]:
    entries = []

    files = list(sorted(pathlib.Path('./entries/').glob('*.html'), reverse=True))

    for i, this_file in enumerate(files):
        kwargs = {}
        kwargs['filename'] = this_file.name

        pagination = {}
        if i > 0:
            pagination['previous'] = files[i - 1].name
        else:
            pagination['previous'] = None
        try:
            pagination['next'] = files[i + 1].name
        except IndexError:
            pagination['next'] = None
        kwargs['pages'] = Pagination(**pagination)

        # parse metadata
        metadata = re.compile(
            r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
            re.MULTILINE)
        with this_file.open() as f:
            content = f.read()
            kwargs['content'] = io.StringIO(content)
            metadata = [(k, v) for k, v in metadata.findall(content)]
            metadata = dict([(k.strip(), v.strip()) for k, v in metadata])

        date = datetime.datetime.strptime(this_file.stem, '%Y-%m-%d')
        kwargs['date'] = date
        kwargs['title'] = date.strftime('%A, %B %-d %Y')
        kwargs['subtitle'] = metadata['title']
        kwargs['banner'] = metadata.get('banner')

        entry = Entry(**kwargs)
        entries.append(entry)

    logger.info('loaded %d entries', len(entries))
    return entries


def clean_webroot():
    www_dir = pathlib.Path('./www/')
    targets = []
    targets += list(www_dir.glob('*.html'))
    targets += list(www_dir.glob('*.xml'))
    for target in targets:
        target.unlink()
        logger.debug('removed old webroot target %s', target.name)
    logger.info('cleaned %d old files from webroot', len(targets))


def load_jinja_env():
    template_dir = pathlib.Path('./templates/')
    loader = jinja2.FileSystemLoader(template_dir)
    count = len(list(template_dir.glob('*.*')))
    logger.debug('loaded %d templates', count)
    return jinja2.Environment(loader=loader)


def main():
    clean_webroot()
    entries = load_entries()
    template = load_jinja_env()


if __name__ == '__main__':
    args = parser.parse_args()
    if args.verbose:
        log_level = logging.DEBUG
    elif args.silent:
        log_level = logging.FATAL
    else:
        log_level = logging.INFO
    log_handler = logging.StreamHandler(stream=sys.stderr)
    log_handler.setLevel(log_level)
    log_formatter = logging.Formatter(fmt='blog: %(message)s')
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    logger.setLevel(log_level)

    start = datetime.datetime.now()
    main()
    duration = (datetime.datetime.now() - start).seconds
    logger.info('program finished in %ds', duration)
