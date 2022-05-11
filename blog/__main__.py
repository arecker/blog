import blog
import collections
import json
import logging
import os
import pathlib

logger = logging.getLogger(__name__)

Info = collections.namedtuple('Info', [
    'author',
    'email',
    'subtitle',
    'title',
    'url',
])


def load_info(dir_data):
    target = pathlib.Path(dir_data) / 'info.json'
    with open(target, 'r') as f:
        kwargs = json.load(f)
        info = Info(**kwargs)
        logger.info('parsed site info from %s', target)
        return info


@blog.register_command
def build(args, info=None):
    """Build the website locally"""
    pave(args)

    info = info or load_info(args.dir_data)

    entries = blog.all_entries(args.dir_entries)
    logger.info('retrieved %d entries from %s', len(entries), args.dir_entries)

    blog.write_sitemap(args.dir_www, full_url=info.url, entries=entries)

    blog.write_feed(args.dir_www,
                    title=info.title,
                    subtitle=info.title,
                    author_name=info.author,
                    author_email=info.email,
                    timestamp=entries[0].date,
                    full_url=info.url,
                    entries=entries[:50])

    blog.write_entries(entries=entries,
                       dir_www=str(args.dir_www),
                       full_url=info.url,
                       author=info.author)

    blog.write_pages(
        dir_www=str(args.dir_www),
        entries=entries,
        full_url=info.url,
        author=info.author,
    )


@blog.register_command
def images(args):
    """Scan site images"""

    blog.scan_images(args.dir_www)


@blog.register_command
def jenkins(args):
    """run the full jenkins pipeline"""

    test(args)
    pave(args)
    build(args)


@blog.register_command
def pave(args):
    """Clean webroot"""

    targets = list(args.dir_www.glob('*.html'))
    targets += list(args.dir_www.glob('*.xml'))
    for target in targets:
        os.remove(target)
        logger.debug('removed old target %s', target)
    logger.info('paved webroot (%d files)', len(targets))


@blog.register_command
def test(args):
    """run the unit test suite"""

    blog.run_test_suite()


def main():
    blog.main()


if __name__ == '__main__':
    main()
