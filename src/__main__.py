import itertools
import logging
import os
import sys

import src as blog

logger = logging.getLogger(__name__)


def main():
    parser = blog.build_argparser()
    args = parser.parse_args()
    blog.configure_logging(verbose=args.verbose, silent=args.silent)
    logger.debug('parsed args %s, ', vars(args))

    # Print help if needed
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)
    elif args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    config = blog.load_config(args.config)
    context = blog.build_global_context(root_directory=args.root_directory,
                                        config=config,
                                        file_wrapper=blog.Page)

    if args.subcommand == 'build':
        pave_webroot(context)
        run_build(config, context)
    elif args.subcommand == 'images':
        blog.resize_all_images(root_directory=context.root_directory)
    elif args.subcommand == 'publish':
        run_publish(config, context)
    elif args.subcommand == 'render':
        run_render(args.source, config, context)
    elif args.subcommand == 'serve':
        blog.start_web_server(context=context)


def run_render(source, config, context):
    if not source.is_absolute():
        source = context.root_directory.joinpath(source)

    for page in itertools.chain(context.pages, context.entries):
        if page.source == source:
            result = page.render(config=config, context=context)
            logger.debug('rendered %s to HTML', page)
            print(result)
            return

    raise ValueError(f'could not find {source} in pages/ nor entries/')


def pave_webroot(context):
    old_files = itertools.chain(context.root_directory.glob('www/*.html'),
                                context.root_directory.glob('www/*.xml'))
    for file in old_files:
        os.remove(file)
        logger.debug('deleting %s', file)


def run_build(config, context):
    blog.build_feeds(config=config, context=context)

    for page in context.pages:
        page.build(context=context, config=config)
        logger.info('rendered %s', page.filename)

    for i, page in enumerate(context.entries):
        page.build(config=config, context=context)
        logger.debug('rendered %s to %s', page, page.target)

        # Log an update every 100 entries and at the end of the list
        if (i + 1) % 100 == 0 or (i + 1) == len(context.entries):
            logger.info('rendered %d out of %d entries', i + 1,
                        len(context.entries))


def run_publish(config, context):
    new_images = filter(blog.is_image,
                        blog.git_new_files(context.root_directory))

    logger.info('checking dimensions for new images: %s', list(new_images))
    for path in new_images:
        blog.check_image(path)

    blog.git_publish_entry(context)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('Unhandled exception!')
        sys.exit(1)
