import sys
import time

import src


def main(args):
    start = time.time()
    site = src.load_site(args)

    logger.info(
        'starting program with python %s (%s)',
        site.python_version,
        sys.executable,
    )

    logger.info(
        'timestamp %s %s',
        site.timestamp.strftime('%Y-%m-%d %H:%m'),
        time.tzname[0]
    )

    logger.info('paved %d old file(s) from webroot', src.pave_webroot())

    # load entries
    entries = src.load_entries()
    logger.info('loaded %s journal entries', len(entries))

    # load pages
    pages = src.load_pages()
    logger.info('loaded %d page(s)', len(pages))

    # load images
    images = src.load_images(entries=entries)
    logger.info('loaded %d image(s)', len(images))

    # create global context
    context = src.make_global_context(
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
    feed_context = context | {
        'items': src.build_feed_items(context)
    }
    with open('./www/feed.xml', 'w') as f:
        content = src.render_template(
            'feed.xml.j2',
            context=feed_context,
        )
        f.write(content)
        logger.info('generated feed.xml')

    duration = time.time() - start
    logger.info('build finished in %.2fs', duration)


if __name__ == '__main__':
    args = src.load_args()
    logger = src.load_logger(verbose=args.verbose)

    try:
        main(args)
    except AssertionError as e:
        logger.error('assertion failed: %s', e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info('program interrupted, exiting')
        sys.exit(0)
