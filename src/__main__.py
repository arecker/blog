import os
import collections
import logging
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

    # Build config and info
    config = src.load_config(args.config)
    entries = list(all_entries())
    pages = list(all_pages())
    info = src.gather_info(entries=entries, pages=pages)

    if args.subcommand == 'build':
        run_build(config, info)
    if args.subcommand == 'migrate':
        run_migrate(info)
    elif args.subcommand == 'render':
        result = render(args.source, config, info)
        print(result)
    elif args.subcommand == 'serve':
        src.start_web_server(root_directory.joinpath('www/'))


def render(source, config, info):
    page = src.Page(source)

    result = src.build_html_page(page=page, config=config, info=info)
    logger.debug('rendered %s to HTML', page)
    return result


TargetGroup = collections.namedtuple('TargetGroup',
                                     ['singular', 'plural', 'targets'])


def run_build(config, info):
    pages = TargetGroup(singular='page', plural='pages', targets=info.pages)
    entries = TargetGroup(singular='entry',
                          plural='entries',
                          targets=info.entries)

    for target_group in [pages, entries]:
        for target in target_group.targets:
            target_path = f'www/{target.filename}'
            with open(target_path, 'w') as f:
                result = src.build_html_page(page=target,
                                             config=config,
                                             info=info)
                f.write(result)
                logger.debug('rendered %s to %s', target, target_path)

        if len(target_group.targets) == 1:
            logger.info('rendered 1 %s', target_group.singular)
        else:
            logger.info('rendered %d %s', len(target_group.targets),
                        target_group.plural)


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
