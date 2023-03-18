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
    'subindex',
])
Pagination = collections.namedtuple('Pagination', ['next', 'previous'])
Context = collections.namedtuple('Context', [
    'page',
    'pages',
    'entries',
    'site',
    'now',
])


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
        kwargs['subindex'] = 'entries.html'

        entry = Page(**kwargs)
        entries.append(entry)

    logger.info('loaded %d entries', len(entries))
    return entries


def load_pages() -> list[Page]:
    pages_dir = pathlib.Path('./pages')
    pages = list(pages_dir.glob('*.html.j2'))
    pages = list(filter(lambda f: f.name != '_layout.html.j2', pages))
    results = []
    for page in pages:
        kwargs = {}
        kwargs['filename'] = page.name[:-3]
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
            kwargs['subindex'] = metadata.get('subindex', None)
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


def render_page(context: Context, sub_jinja=True) -> str:
    content = context.page.content.read()
    if sub_jinja:
        # render content as a sub jinja template
        content = jinja2.Environment().from_string(content)
        content = content.render(content=content, **context._asdict())

    # render layout around content
    with pathlib.Path('./pages/_layout.html.j2').open('r') as layout:
        layout = jinja2.Environment().from_string(layout.read())
        return layout.render(content=content, **context._asdict())


def main():
    clean_webroot()

    entries = load_entries()
    pages = load_pages()
    site = Site(
        protocol='https',
        domain='www.alexrecker.com',
        author='Alex Recker',
    )
    now = datetime.datetime.now()

    for i, page in enumerate(pages):
        context = Context(
            page=page,
            pages=pages,
            entries=entries,
            site=site,
            now=now,
        )
        content = render_page(context)
        with pathlib.Path(f'./www/{page.filename}').open('w') as target:
            target.write(content)
        logger.info('rendered %s (%d/%d)', page.filename, i + 1, len(pages))

    count = len(entries)
    for i, entry in enumerate(entries):
        context = Context(
            page=entry,
            pages=pages,
            entries=entries,
            site=site,
            now=now,
        )
        content = render_page(context, sub_jinja=False)
        with pathlib.Path(f'./www/{entry.filename}').open('w') as target:
            target.write(content)
        if (i + 1) % 100 == 0:
            logger.info('rendered %d/%d entries', i + 1, count)


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
