import logging
import collections
import sys

import blog

logger = logging.getLogger(__name__)


def main():
    """The main routine.

    Parse global args and call the right function based on the
    subcommand.
    """

    default_config_path = str(blog.root_directory.joinpath('blog.conf'))

    # Parse arguments
    parser = blog.build_argparser(default_config_path)
    args = parser.parse_args()

    # Setup logging
    blog.configure_logging(verbose=args.verbose, silent=args.silent)

    logger.debug('parsed args %s', vars(args))

    # Print help if needed
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)
    elif args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    # Build config and info
    config = blog.load_config(args.config)
    entries = list(all_entries())
    pages = list(all_pages())
    info = blog.gather_info(entries=entries, pages=pages)

    if args.subcommand == 'build':
        run_build(config, info)
    elif args.subcommand == 'render':
        result = render(args.source, config, info)
        print(result)
    elif args.subcommand == 'serve':
        blog.start_web_server(blog.root_directory.joinpath('www/'))


def render(source, config, info):
    page = blog.Page(source)

    result = blog.build_html_page(page=page, config=config, info=info)
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
                result = blog.build_html_page(page=target,
                                              config=config,
                                              info=info)
                f.write(result)
                logger.debug('rendered %s to %s', target, target_path)
        if len(target_group.targets) == 1:
            logger.info('rendered 1 %s -> %s', target_group.singular,
                        target_path)
        else:
            logger.info('rendered %d %s -> %s', len(target_group),
                        target_group.plural, target_path)
        logger.info('built %d page(s)', len(info.pages))


def all_entries():
    for path in sorted(blog.root_directory.glob('entries/*.*')):
        yield blog.Page(path)


def all_pages():
    for path in sorted(blog.root_directory.glob('pages/*.*')):
        yield blog.Page(path)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
