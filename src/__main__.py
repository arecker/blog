import argparse
import collections
import logging
import os
import pathlib
import random

from . import (
    config,
    feed,
    lib,
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


@lib.register_page(filename='media.html', title='Media', description='all website media')
def media_page(renderer=None, args=None, **kwargs):
    renderer.block('h3', contents='Index')
    sections = ('Images', 'Videos', 'Audio')
    with renderer.wrapping_block('ul'):
        for section in sections:
            with renderer.wrapping_block('li'):
                renderer.block('a', href='#' + section.lower(), contents=section)

    media = collections.defaultdict(list)
    for p in pathlib.Path(args.dir_www).glob('**/*.*'):
        if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.bmp'):
            media['images'].append(p)
        if p.suffix.lower() in ('.ogg', '.mp3', '.wav'):
            media['audio'].append(p)
        if p.suffix.lower() in ('.mp4', '.webm'):
            media['videos'].append(p)

    for section in ('images', 'videos', 'audio'):
        renderer.block('h3', contents=section.title(), _id=section)
        total_size = sum([os.path.getsize(i) for i in media[section]])
        renderer.table(data=[
            ['Total Count', str(len(media[section]))],
            ['Total Storage', lib.convert_size(total_size)]
        ])

        with renderer.wrapping_block('table'):
            with renderer.wrapping_block('tr'):
                renderer.block('td', contents='Name')
                renderer.block('td', contents='Size')
            for item in sorted(media[section], key=lambda p: p.name, reverse=True):
                with renderer.wrapping_block('tr'):
                    with renderer.wrapping_block('td'):
                        href = './' + str(
                            item.relative_to(pathlib.Path(args.dir_www)))
                        renderer.block('a', href=href, contents=item.name)

                    renderer.block('td',
                                   contents=lib.convert_size(
                                   os.path.getsize(item)))

    return renderer.text


@lib.register_page(filename='404.html', title='404', description='page not found')
def four_oh_four(renderer=None, entries=[], **kwargs):
    choice = random.choice([e for e in entries if e.banner])
    renderer.block('p', 'I don\'t have that page, so here\'s a random entry instead!')
    renderer.figure(alt='random banner',
                    src=f'./images/banners/{choice.banner}',
                    href=f'./{choice.filename}',
                    caption=choice.description)
    return renderer.text


@lib.register_page(filename='index.html',
                   title='Hey Reader!',
                   description='emails from Alex')
def index(renderer=None, args=None, entries=[], pages=[]):
    latest = entries[0]
    renderer.block('h2', 'Latest Entry')
    renderer.figure(alt='latest entry banner',
                    src=f'./images/banners/{latest.banner}',
                    href=f'./{latest.filename}',
                    caption=latest.description)

    renderer.block('h2', 'Pages')
    pages = [p for p in pages if p.filename not in ('index.html', '404.html')]
    with renderer.wrapping_block('table'):
        for page in pages:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    renderer.block('a',
                                   href=f'./{page.filename}',
                                   contents=page.filename)
                renderer.block('td', contents=page.description)

    renderer.block('h2', 'Entries')
    with renderer.wrapping_block('table'):
        for entry in entries:
            with renderer.wrapping_block('tr'):
                with renderer.wrapping_block('td'):
                    renderer.block('a',
                                   href=f'./{entry.filename}',
                                   contents=f'{entry.filename}')
                    renderer.block('td', contents=entry.description)

    return renderer.text


def main(args):
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
    logger.debug('loaded config %s', c)

    feed.write(
        www_dir=c.site.www,
        title=c.site.title,
        subtitle=c.site.subtitle,
        author_name=c.site.name,
        author_email=c.site.email,
        url=c.site.url,
        entries=entries,
    )

    lib.validate_website(args.dir_www)


if __name__ == '__main__':
    args = parser.parse_args()
    utils.configure_logging(verbose=args.verbose)
    main(args=args)
