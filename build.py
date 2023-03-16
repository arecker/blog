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
import jinja2.ext


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='store_true')
group.add_argument('-s', '--silent', action='store_true')

Site = collections.namedtuple('Site', [
    'protocol',
    'domain',
    'author',
])


Page = collections.namedtuple('Page', [
    'filename',
    'title',
    'subtitle',
    'date',
    'banner',
    'content',
    'next',
    'previous',
])
Pagination = collections.namedtuple('Pagination', ['next', 'previous'])


class Now(jinja2.ext.Extension):
    def __init__(self, environment):
        super().__init__(environment)

        # add the defaults to the environment
        environment.extend(now=datetime.datetime.now())

    # def parse(self, parser):
    #     # the first token is the token that started the tag.  In our case
    #     # we only listen to ``'cache'`` so this will be a name token with
    #     # `cache` as value.  We get the line number so that we can give
    #     # that line number to the nodes we create by hand.
    #     lineno = next(parser.stream).lineno

    #     # now we parse a single expression that is used as cache key.
    #     args = [parser.parse_expression()]

    #     # if there is a comma, the user provided a timeout.  If not use
    #     # None as second parameter.
    #     if parser.stream.skip_if("comma"):
    #         args.append(parser.parse_expression())
    #     else:
    #         args.append(nodes.Const(None))

    #     # now we parse the body of the cache block up to `endcache` and
    #     # drop the needle (which would always be `endcache` in that case)
    #     body = parser.parse_statements(["name:endcache"], drop_needle=True)

    #     # now return a `CallBlock` node that calls our _cache_support
    #     # helper method on this extension.
    #     return nodes.CallBlock(
    #         self.call_method("_cache_support", args), [], [], body
    #     ).set_lineno(lineno)

    # def _cache_support(self, name, timeout, caller):
    #     """Helper callback."""
    #     key = self.environment.fragment_cache_prefix + name

    #     # try to load the block from the cache
    #     # if there is no fragment in the cache, render it and store
    #     # it in the cache.
    #     rv = self.environment.fragment_cache.get(key)
    #     if rv is not None:
    #         return rv
    #     rv = caller()
    #     self.environment.fragment_cache.add(key, rv, timeout)
    #     return rv


def parse_metadata(content):
    metadata = re.compile(
        r'^\s?<!--\s?meta:(?P<key>[A-za-z]+)\s?(?P<value>.*)\s?-->$',
        re.MULTILINE)
    metadata = [(k, v) for k, v in metadata.findall(content)]
    metadata = dict([(k.strip(), v.strip()) for k, v in metadata])
    return metadata


def paginate_entry(files, i) -> Pagination:
    kwargs = {}
    if i > 0:
        kwargs['previous'] = files[i - 1].name
    else:
        kwargs['previous'] = None
    try:
        kwargs['next'] = files[i + 1].name
    except IndexError:
        kwargs['next'] = None
    return Pagination(**kwargs)


def load_entries() -> list[Page]:
    entries = []

    files = list(sorted(pathlib.Path('./entries/').glob('*.html'), reverse=True))

    for i, this_file in enumerate(files):
        kwargs = {}
        kwargs['filename'] = this_file.name

        pagination = paginate_entry(files, i)
        kwargs['next'] = pagination.next
        kwargs['previous'] = pagination.previous

        with this_file.open() as f:
            content = f.read()
            kwargs['content'] = io.StringIO(content)
            metadata = parse_metadata(content)

        date = datetime.datetime.strptime(this_file.stem, '%Y-%m-%d')
        kwargs['date'] = date
        kwargs['title'] = date.strftime('%A, %B %-d %Y')
        kwargs['subtitle'] = metadata['title']
        kwargs['banner'] = metadata.get('banner')

        entry = Page(**kwargs)
        entries.append(entry)

    logger.info('loaded %d entries', len(entries))
    return entries


def load_pages() -> list[Page]:
    pages_dir = pathlib.Path('./pages')
    pages = list(pages_dir.glob('*.html.j2'))
    results = []
    for page in pages:
        kwargs = {}
        kwargs['filename'] = page.name
        kwargs['date'] = None

        with page.open('r') as f:
            content= f.read()
            kwargs['content'] = io.StringIO(content)
            metadata = parse_metadata(content)
            kwargs['title'] = metadata['title']
            kwargs['subtitle'] = metadata['subtitle']
            kwargs['banner'] = metadata.get('banner')
            kwargs['previous'] = metadata.get('previous')
            kwargs['next'] = metadata.get('previous')
        results.append(Page(**kwargs))

    logger.info('loaded %d page(s)', len(pages))
    return results


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
    return jinja2.Environment(loader=loader, extensions=[Now])


def main():
    clean_webroot()
    template = load_jinja_env()
    entries = load_entries()
    pages = load_pages()


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

    main()
    logger.info('program finished')
