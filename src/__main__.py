import argparse
import logging
import pathlib
import sys
import time
import datetime

from . import (
    render_page,
    load_entries,
    load_pages,
    make_global_context,
)


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()

group = parser.add_argument_group('Site Options')
group.add_argument('--site-protocol', default='https')
group.add_argument('--site-domain', required=True)
group.add_argument('--site-author', required=True)


def main(args):
    start = time.time()

    # load entries
    entries = load_entries()
    logger.info('loaded %s journal entries', len(entries))

    # load pages
    pages = load_pages()
    logger.info('loaded %s page(s)', len(pages))

    # create global context
    context = make_global_context(
        args=args,
        entries=entries,
        pages=pages,
    )

    for page in pages:
        with open(f'./www/{page.filename}', 'w') as f:
            f.write(render_page(page, context))
        logger.info('generated %s', page.filename)

    # render entries
    total = len(entries)
    for i, entry in enumerate(entries):
        with open(f'./www/{entry.filename}', 'w') as f:
            f.write(render_page(entry, context))

        if ((i + 1) % 100 == 0) or (i + 1) == total:
            logger.info('generated %d/%d journal entries', i + 1, total)

    duration = time.time() - start
    logger.info('build finished in %ds', duration)


if __name__ == '__main__':
    logging.basicConfig(
        stream=sys.stderr,
        format='blog: %(message)s',
        level=logging.INFO,
    )

    args = parser.parse_args()

    try:
        main(args)
    except AssertionError as e:
        logger.error('assertion failed: %s', e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info('program interrupted, exiting')
        sys.exit(0)
