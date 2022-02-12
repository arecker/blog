"""generate journal archives"""

import logging
import random
import urllib.parse

from .. import utils

logger = logging.getLogger(__name__)


def regiser(parser):
    return parser


def render_entries_page(entries=[],
                        full_url=None,
                        nav=[],
                        year=None,
                        author=''):
    html = utils.StringWriter(starting_indent=4)
    html.comment('RSS Feed')
    with html.block('p', blank=True):
        link = full_url.geturl()
        link = urllib.parse.urljoin(link, 'feed.xml')
        link = urllib.parse.quote_plus(link)
        link = f'https://validator.w3.org/feed/check.cgi?url={link}'
        with html.block('a', href=link):
            src = './assets/valid-atom.png'
            title = 'Validate my Atom 1.0 feed'
            alt = '[Valid Atom 1.0]'
            html.write(f'<img src="{src}" alt="{alt}" title="{title}">')

    with html.block('p', blank=True):
        html.write(
            'RSS feed available here: <a href="./feed.xml">feed.xml</a>')

    years = set([e.date.year for e in entries])

    html.comment('Year Archives')
    with html.block('nav', blank=True):
        with html.block('span'):
            for y in sorted(years, reverse=True):
                html.write(f'<a href="./{y}.html">{y}.html</a>')

    html.comment('Random Banner')
    choice = random.choice([e for e in entries if e.banner])
    link = f'<a href="./{choice.filename}">{choice.title}</a>'
    caption = f'Taken from {link}, "{choice.description}"'
    html.figure(src=f'./images/banners/{choice.banner}', caption=caption)

    page = utils.Page('entries.html', 'Entries',
                      'Complete Archive of Journal Entries', None)
    return utils.render_page(page,
                             full_url,
                             content=html.text.rstrip(),
                             nav_pages=nav,
                             year=year,
                             author=author)


def main(args, entries=[], nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    entries = entries or utils.fetch_entries(args.directory / 'entries')

    output = render_entries_page(entries=entries,
                                 full_url=args.full_url,
                                 nav=nav,
                                 year=args.year,
                                 author=args.author)
    with open(args.directory / 'www/entries.html', 'w') as f:
        f.write(output)
    logger.info('generated entries.html')
