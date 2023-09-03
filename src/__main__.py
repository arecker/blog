import sys
import time

from . import (
    load_args,
    load_entries,
    load_feed,
    load_images,
    load_logger,
    load_pages,
    load_site,
    make_global_context,
    pave_webroot,
)


def main(args):
    start = time.time()
    site = load_site(args)

    logger.info(
        'starting program with python %s (%s)',
        site.python_version,
        site.python_executable,
    )

    logger.info(
        'timestamp %s %s',
        site.timestamp.strftime('%Y-%m-%d %H:%m'),
        time.tzname[0]
    )

    logger.info('paved %d old file(s) from webroot', pave_webroot())

    # load entries
    entries = load_entries()
    logger.info('loaded %s journal entries', len(entries))

    # load pages
    pages = load_pages()
    logger.info('loaded %d page(s)', len(pages))

    # load images
    images = load_images(entries=entries)
    logger.info('loaded %d image(s)', len(images))

    # create global context
    context = make_global_context(
        site=site,
        entries=entries,
        pages=pages,
        images=images,
    )._asdict()

    for page in pages:
        page.write(context=context)
        logger.info('generated %s', page.filename)

    # render entries
    total = len(entries)
    for i, entry in enumerate(entries):
        entry.write(context=context)
        if ((i + 1) % 100 == 0) or (i + 1) == total:
            logger.info('generated %d/%d journal entries', i + 1, total)

    # render feed
    feed = load_feed(site, entries=entries, images=images)
    feed.write()
    logger.info('generated feed.xml')

    duration = time.time() - start
    logger.info('build finished in %.2fs', duration)


if __name__ == '__main__':
    args = load_args()
    logger = load_logger(verbose=args.verbose)

    try:
        main(args)
    except AssertionError as e:
        logger.error('assertion failed: %s', e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info('program interrupted, exiting')
        sys.exit(0)
