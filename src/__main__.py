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

    # Build config, target groups, and info
    config = src.load_config(args.config)

    # Build target groups
    entries = src.entries_target_group(root_directory, src.Page)
    pages = src.pages_target_group(root_directory, src.Page)

    # Build info
    context = src.build_global_context(entries=entries.targets,
                                       pages=pages.targets)

    if args.subcommand == 'build':
        pave_webroot()
        run_build(config, context, entries=entries, pages=pages)
    if args.subcommand == 'migrate':
        run_migrate(context)
    elif args.subcommand == 'render':
        result = render(args.source, config, context)
        print(result)
    elif args.subcommand == 'serve':
        src.start_web_server(root_directory.joinpath('www/'))


def render(source, config, context):
    page = src.Page(source)

    result = src.build_html_page(page=page, config=config, context=context)
    logger.debug('rendered %s to HTML', page)
    return result


def build_feeds(config, entries, context):
    with open('www/feed.xml', 'w') as f:
        f.write(
            src.build_rss_feed(config=config,
                               entries=entries.targets,
                               context=context))
    logger.info('rendered feed.xml')

    with open('www/sitemap.xml', 'w') as f:
        f.write(src.build_sitemap(context=context))
    logger.info('rendered sitemap.xml')


def pave_webroot():
    old_files = itertools.chain(root_directory.glob('www/*.html'),
                                root_directory.glob('www/*.xml'))
    for file in old_files:
        os.remove(file)
        logger.debug('deleting %s', file)


def run_build(config, context, entries=None, pages=None):
    for target_group in [pages, entries]:
        for target in target_group.targets:
            target_path = f'www/{target.filename}'
            with open(target_path, 'w') as f:
                result = src.build_html_page(page=target,
                                             config=config,
                                             context=context)
                f.write(result)
                logger.debug('rendered %s to %s', target, target_path)

        if len(target_group.targets) == 1:
            logger.info('rendered 1 %s', target_group.singular)
        else:
            logger.info('rendered %d %s', len(target_group.targets),
                        target_group.plural)

    build_feeds(config, entries, context)


def run_migrate(info):
    for entry in info.entries:
        if not entry.is_markdown():
            continue

        metadata = '\n'.join(
            [f'<!-- meta:{k} {v} -->' for k, v in entry.metadata.items()])

        with open(root_directory.joinpath('entries/', entry.filename),
                  'w') as f:
            f.write(metadata + '\n\n')
            f.write(entry.content)

        logger.info('migrated %s from markdown', entry)


def all_entries():
    for path in sorted(root_directory.glob('entries/*.*')):
        yield src.Page(path)


def all_pages():
    for path in sorted(root_directory.glob('pages/*.*')):
        yield src.Page(path)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
