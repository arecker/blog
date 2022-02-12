"""generate journal archives"""

import logging
import random
import urllib.parse

from .. import utils

logger = logging.getLogger(__name__)


def regiser(parser):
    return parser


def main(args):
    html = utils.StringWriter(starting_indent=4)
    entries = utils.fetch_entries(args.directory / 'entries')

    html.comment('RSS Feed')
    with html.block('span', blank=True):
        link = args.full_url.geturl()
        link = urllib.parse.urljoin(link, 'feed.xml')
        link = urllib.parse.quote_plus(link)
        link = f'https://validator.w3.org/feed/check.cgi?url={link}'
        with html.block('a', href=link):
            src = './assets/valid-atom.png'
            title = 'Validate my Atom 1.0 feed'
            alt = '[Valid Atom 1.0]'
            html.write(f'<img src="{src}" alt="{alt}" title="{title}">')
    html.write('<br/>')
    html.write('RSS feed available here: <a href="./feed.xml">feed.xml</a>')

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

    nav = utils.read_nav(args.directory / 'data')
    page = utils.Page('entries.html', 'Entries',
                      'Complete Archive of Journal Entries', None)
    content = utils.render_page(page,
                                args.full_url,
                                content=html.text.rstrip(),
                                nav_pages=nav,
                                year=args.year,
                                author=args.author)

    with open(args.directory / 'www/entries.html', 'w') as f:
        f.write(content)
    logger.info('generated entries.html')
