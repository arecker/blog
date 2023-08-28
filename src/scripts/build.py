import argparse
import datetime
import logging
import platform
import sys
import time

import src


logger = logging.getLogger('blog')

parser = argparse.ArgumentParser(
    'src.scripts.build',
    description='Build the website to the local file system',
)
group = parser.add_argument_group('Run options')
group.add_argument(
    '--verbose',
    default=False,
    action='store_true',
    help='print debug logs'
)

group = parser.add_argument_group('Directories')
group.add_argument('--dir-www', default='./www')
group.add_argument('--dir-entries', default='./entries')
group.add_argument('--dir-pages', default='./pages')
group.add_argument('--dir-templates', default='./templates')
group.add_argument('--dir-images', default='./www/images')

group = parser.add_argument_group('Site Options')
group.add_argument('--site-title', required=True)
group.add_argument('--site-description', required=True)
group.add_argument('--site-protocol', default='https')
group.add_argument('--site-domain', required=True)
group.add_argument('--site-author', required=True)
group.add_argument('--site-email', required=True)


def main(args):
    start = time.time()
    logger.info(
        'starting program with python v%s (%s)',
        platform.python_version(),
        sys.executable,
    )
    logger.info(
        'timestamp %s %s',
        datetime.datetime.now().strftime('%Y-%m-%d %H:%m'),
        time.tzname[0]
    )

    logger.info('paved %d old file(s) from webroot', src.pave_webroot())

    # load entries
    entries = src.Page.load_entries()
    logger.info('loaded %s journal entries', len(entries))

    # load pages
    pages = src.Page.load_pages()
    logger.info('loaded %d page(s)', len(pages))

    # load images
    images = src.load_images(entries=entries)
    logger.info('loaded %d image(s)', len(images))

    # create global context
    context = src.make_global_context(
        args=args,
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
    args = parser.parse_args()
    src.configure_logging(logger, verbose=args.verbose)

    try:
        main(args)
    except AssertionError as e:
        logger.error('assertion failed: %s', e)
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info('program interrupted, exiting')
        sys.exit(0)
