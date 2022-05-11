import argparse
import collections
import json
import logging
import pathlib

from .entries import all_entries, write_entries
from .feed import write_feed
from .pages import write_pages
from .sitemap import write_sitemap

logger = logging.getLogger('build')

parser = argparse.ArgumentParser()
parser.add_argument('--dir-data', required=True)
parser.add_argument('--dir-entries', required=True)
parser.add_argument('--dir-www', required=True)

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


def main():
    args = parser.parse_args()

    info = load_info(args.dir_data)
    entries = all_entries(args.dir_entries)
    logger.info('retrieved %d entries from %s', len(entries), args.dir_entries)
    write_sitemap(args.dir_www, full_url=info.url, entries=entries)

    write_feed(args.dir_www,
               title=info.title,
               subtitle=info.title,
               author_name=info.author,
               author_email=info.email,
               timestamp=entries[0].date,
               full_url=info.url,
               entries=entries[:50])

    write_entries(entries=entries,
                  dir_www=str(args.dir_www),
                  full_url=info.url,
                  author=info.author)

    write_pages(
        dir_www=str(args.dir_www),
        entries=entries,
        full_url=info.url,
        author=info.author,
    )


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    main()
