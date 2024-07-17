import pathlib
import sys
import time

import src


def main(args):
    start = time.time()
    site = src.load_site(args)

    logger.info(
        'starting program with python %s at %s',
        site.python_version,
        site.timestamp.strftime('%Y-%m-%d %H:%m'),
    )

    # run unit tests
    logger.info('executed %d test(s)', src.run_unit_tests())

    # clean up old files
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

    # load spiders
    spiders = src.load_spiders(data_dir=args.dir_data, images=images)
    logger.info('loaded %d spider(s)', len(spiders))

    # create global context
    context = {
        'site': site,
        'entries': entries,
        'pages': pages,
        'images': images,
        'spiders': spiders,
    }

    for page in pages:
        page.write(context=context)
        logger.info('generated %s', page.filename)

    # render entries
    for i, entry in enumerate(entries):
        entry.write(context=context)
    logger.info('generated %d journal(s)', len(entries))

    # render feed
    feed = src.load_feed(site, entries=entries, images=images)
    feed.write()
    logger.info('generated feed.xml')

    # render api docs
    logger.info('generated api docs - %d file(s)', src.write_api_docs())

    # validate HTML files
    total = 0
    files = list(pathlib.Path('./www/').glob('*.html'))
    for path in files:
        total += src.validate_html_references(path)
    logger.info('validated %d total reference(s) across %d file(s)',
                total, len(files))

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
