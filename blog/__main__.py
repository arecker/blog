import blog
import logging

logger = logging.getLogger(__name__)


@blog.register_command
def build(args):
    """Build the website locally"""

    entries = blog.all_entries(args.dir_entries)
    logger.info('retrieved %d entries from %s', len(entries), args.dir_entries)

    blog.write_sitemap(args.dir_www, full_url=args.site_url, entries=entries)

    # blog.write_feed(args.dir_www)

    blog.write_entries(entries,
                       dir_www=str(args.dir_www),
                       full_url=str(args.site_url),
                       author=args.site_author,
                       year=args.site_year)


def main():
    blog.main()


if __name__ == '__main__':
    main()
