import argparse
import logging

from . import pages as _  # noqa:F401
from . import lib

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--dir-data', required=True)
parser.add_argument('--dir-entries', required=True)
parser.add_argument('--dir-www', required=True)


def main():
    args = parser.parse_args()

    info = lib.load_info(args.dir_data)
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
