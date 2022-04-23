import blog
import logging

logger = logging.getLogger(__name__)


@blog.register_command
def build(args):
    """Build the website locally"""

    entries = blog.all_entries(args.dir_entries)
    if len(entries) == 1:
        logger.info('retrieved 1 entry from %s', args.dir_entries)
    else:
        logger.info('retrieved %d entries from %s', len(entries),
                    args.dir_entries)

    for i, entry in enumerate(entries):
        with open(entry.source, 'r') as f:
            content = f.read()

        content = blog.render_page(page=entry,
                                   content=content,
                                   full_url=str(args.site_url),
                                   author=args.site_author)

        target = args.dir_www / entry.filename
        with open(target, 'w') as f:
            f.write(content)
            logger.debug('rendered %s', target)

        if i % 100 == 0:
            logger.info('rendered %d out of %d entries', i + 1, len(entries))


def main():
    blog.main()


if __name__ == '__main__':
    main()
