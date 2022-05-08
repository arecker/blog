import blog
import logging

logger = logging.getLogger(__name__)


@blog.register_command
def build(args):
    """Build the website locally"""

    entries = blog.all_entries(args.dir_entries)
    logger.info('retrieved %d entries from %s', len(entries), args.dir_entries)

    blog.write_sitemap(args.dir_www, full_url=args.site_url, entries=entries)

    blog.write_feed(args.dir_www,
                    title=args.site_title,
                    subtitle=args.site_subtitle,
                    author_name=args.site_author,
                    author_email=args.site_email,
                    timestamp=entries[0].date,
                    full_url=args.site_url.geturl(),
                    entries=entries[:50])

    blog.write_entries(entries=entries,
                       dir_www=str(args.dir_www),
                       full_url=str(args.site_url),
                       author=args.site_author,
                       year=args.site_year)

    blog.write_pages(
        dir_www=str(args.dir_www),
        entries=entries,
        full_url=str(args.site_url),
        year=args.site_year,
    )


@blog.register_command
def images(args):
    """Scan site images"""

    blog.scan_images(args.dir_www)


def main():
    blog.main()


if __name__ == '__main__':
    main()
