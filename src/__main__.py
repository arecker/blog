import itertools
import logging
import os
import pathlib
import sys

import src

logger = logging.getLogger(__name__)

this_directory = os.path.dirname(os.path.realpath(__file__))
root_directory = pathlib.Path(
    os.path.abspath(os.path.join(this_directory, '../')))


def main():
    """The main routine.

    Parse global args and call the right function based on the
    subcommand.
    """

    default_config_path = str(root_directory.joinpath('blog.conf'))

    # Parse arguments
    parser = src.build_argparser(default_config_path)
    args = parser.parse_args()

    # Setup logging
    src.configure_logging(verbose=args.verbose, silent=args.silent)

    logger.debug('parsed args %s, running from %s', vars(args), root_directory)

    # Print help if needed
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)
    elif args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    config = src.load_config(args.config)
    entries = list(src.all_entries(root_directory))
    pages = list(src.all_pages(root_directory))
    context = src.build_global_context(root_directory=root_directory,
                                       config=config,
                                       entries=entries,
                                       pages=pages)

    if args.subcommand == 'build':
        pave_webroot()
        run_build(config, context)
    elif args.subcommand == 'images':
        src.resize_all_images(root_directory=context.root_directory)
    elif args.subcommand == 'publish':
        run_publish(config, context)
    elif args.subcommand == 'render':
        result = render(args.source, config, context)
        print(result)
    elif args.subcommand == 'serve':
        src.start_web_server(context=context)


def render(source, config, context):
    if not source.is_absolute():
        source = context.root_directory.joinpath(source)

    for page in itertools.chain(context.pages, context.entries):
        if page.source == source:
            result = page.render(config=config, context=context)
            logger.debug('rendered %s to HTML', page)
            return result

    raise ValueError(f'could not find {source} {root_directory}')


def pave_webroot():
    old_files = itertools.chain(root_directory.glob('www/*.html'),
                                root_directory.glob('www/*.xml'))
    for file in old_files:
        os.remove(file)
        logger.debug('deleting %s', file)


def run_build(config, context):
    for i, page in enumerate(context.entries):
        page.build(config=config, context=context)
        logger.debug('rendered %s to %s', page, page.target)

        # Log an update every 100 entries and at the end of the list
        if (i + 1) % 100 == 0 or (i + 1) == len(context.entries):
            logger.info('rendered %d out of %d entries', i + 1,
                        len(context.entries))

    for page in context.pages:
        page.build(context=context, config=config)
        logger.info('rendered %s', page.filename)

    with open('www/feed.xml', 'w') as f:
        f.write(src.build_rss_feed(config=config, context=context))
    logger.info('rendered feed.xml')

    with open('www/sitemap.xml', 'w') as f:
        f.write(src.build_sitemap(context=context))
    logger.info('rendered sitemap.xml')


def run_publish(config, context):
    new_files = src.git_new_files(context.root_directory)
    logger.debug('found new unstaged files %s', new_files)

    for image_file in filter(src.is_image, new_files):
        src.check_image(image_file)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
