import logging
import argparse

from . import pages as _  # noqa:F401
from . import (
    config,
    feed,
    lib,
    template,
    utils,
)


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog='python -m src')
group = parser.add_argument_group('run options')
group.add_argument('--verbose', action='store_true', default=False, help='show debug logs')
group.add_argument('-C', '--config', help='path to config file', default='./blog.conf')
group = parser.add_argument_group('resource directories')
group.add_argument('--dir-data', required=True)
group.add_argument('--dir-entries', required=True)
group.add_argument('--dir-www', required=True)
group = parser.add_argument_group('one-off subcommands (exit immediately)')
group.add_argument('--hook', action='store_true', default=False, help='run git pre-commit hook')


def main(args):
    if args.hook:
        lib.run_pre_commit_hook()
        return

    info = lib.load_info(args.dir_data)
    entries = lib.fetch_entries(args.dir_entries)
    pages = lib.fetch_pages()

    utils.pave_webroot(www_dir=args.dir_www)

    lib.write_sitemap(args.dir_www,
                      full_url=info.url,
                      entries=entries,
                      pages=[p.filename for p in pages])

    lib.write_feed(args.dir_www,
                   title=info.title,
                   subtitle=info.title,
                   author_name=info.author,
                   author_email=info.email,
                   timestamp=entries[0].date,
                   full_url=info.url,
                   entries=entries[:50])

    lib.write_entries(entries=entries,
                      dir_www=str(args.dir_www),
                      full_url=info.url,
                      author=info.author)

    lib.write_pages(
        dir_www=str(args.dir_www),
        entries=entries,
        pages=pages,
        full_url=info.url,
        author=info.author,
        args=args,
    )

    c = config.load(args.config)

    feed.write(
        www_dir=c.site.www,
        title=c.site.title,
        subtitle=c.site.subtitle,
        author_name=c.site.name,
        author_email=c.site.email,
        url=c.site.url,
        entries=entries,
    )

    content = template.render(template_path=c.site.template, context={
        'site': c.site,
        'page': pages[0],
    })
    logger.debug('loaded config %s', c)


    lib.validate_website(args.dir_www)


if __name__ == '__main__':
    args = parser.parse_args()
    utils.configure_logging(verbose=args.verbose)
    main(args=args)
