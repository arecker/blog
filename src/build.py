import argparse
import collections
import json
import logging
import pathlib

from . import lib
from . import pages as _  # noqa:F401

logger = logging.getLogger(__name__)

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
    entries = lib.fetch_entries(args.dir_entries)
    pages = lib.fetch_pages()

    lib.write_sitemap(args.dir_www,
                      full_url=info.url,
                      entries=entries,
                      pages=[p.filename for p in pages])

    lib.write_feed(args.dir_www,
                   title=info.title,
                   subtitle=info.title,
                   author_name=info.author,
                   author_email=info.email,
                   timestamp=entries[0].date,
                   full_url=info.url,
                   entries=entries[:50])

    lib.write_entries(entries=entries,
                      dir_www=str(args.dir_www),
                      full_url=info.url,
                      author=info.author)

    lib.write_pages(
        dir_www=str(args.dir_www),
        entries=entries,
        pages=pages,
        full_url=info.url,
        author=info.author,
        args=args,
    )


if __name__ == '__main__':
    lib.configure_logging()
    main()
