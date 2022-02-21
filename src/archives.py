"""generate journal archives"""

import logging
import random
import urllib.parse

from . import utils

logger = logging.getLogger(__name__)


def render_feed_link(html: utils.StringWriter,
                     full_url: urllib.parse.ParseResult):
    html.write(f'<h2>Follow with RSS</h2>')
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

    return html


def render_years_nav(html: utils.StringWriter, years=[]):
    html.write(f'<h2>Browse by Year</h2>')
    with html.block('nav', blank=True):
        with html.block('span'):
            for y in sorted(years, reverse=True):
                html.write(f'<a href="./{y}.html">{y}.html</a>')
    return html


def render_randoms(html: utils.StringWriter, choices: list[utils.Entry]):
    html.write('<h2>Browse Some Random Entries</h2>')
    for choice in choices:
        link = f'Taken from <a href="./{choice.filename}">{choice.description}</a>'
        html.figure(src=f'./images/banners/{choice.banner}', caption=link, alt='banner image from a random entry')
    return html


def render_entries_table(html: utils.StringWriter, entries=[]):
    with html.block('table'):
        for entry in entries:
            with html.block('tr'):
                with html.block('td'):
                    html.write(
                        f'<a href="./{entry.filename}">{entry.filename}</a>')
                html.write(f'<td>{entry.description}</td>')

    return html


def render_entries_page(entries=[],
                        full_url=None,
                        nav=[],
                        year=None,
                        author='',
                        years=[]):

    html = utils.StringWriter(starting_indent=4)
    html = render_feed_link(html, full_url)
    html = render_years_nav(html, years=years)
    choices = random.sample([e for e in entries if e.banner], 3)
    html = render_randoms(html, choices)

    page = utils.Page('entries.html', 'Entries',
                      'Complete Archive of Journal Entries', None)
    return utils.render_page(page,
                             full_url,
                             content=html.text.rstrip(),
                             nav_pages=nav,
                             author=author)


def render_year_page(year=None,
                     entries=[],
                     full_url=None,
                     nav=[],
                     author='',
                     years=[]):
    html = utils.StringWriter(starting_indent=4)
    html = render_feed_link(html, full_url)

    try:
        choices = random.sample([e for e in entries if e.banner], 3)
        html = render_randoms(html, choices)
    except ValueError:  # no banners to pick from!
        pass
    
    html = render_years_nav(html, years=years)
    html.br()
    html = render_entries_table(html, entries)

    page = utils.Page(f'{year}.html', str(year), f'All Entries from {year}',
                      None)
    return utils.render_page(page,
                             full_url,
                             content=html.text.rstrip(),
                             nav_pages=nav,
                             author=author)


def main(args, entries=[], nav=[]):
    nav = nav or utils.read_nav(args.directory / 'data')
    entries = entries or utils.fetch_entries(args.directory / 'entries')
    years = set([e.date.year for e in entries])

    output = render_entries_page(entries=entries,
                                 full_url=args.full_url,
                                 nav=nav,
                                 author=args.author,
                                 years=years)

    with utils.write_page(args.directory,
                          'entries.html',
                          overwrite_ok=args.overwrite) as f:
        f.write(output)
    logger.info('generated entries.html')

    for year in set([e.date.year for e in entries]):
        year_entries = [e for e in entries if e.date.year == year]
        output = render_year_page(
            year=year,
            entries=year_entries,
            full_url=args.full_url,
            nav=nav,
            author=args.author,
            years=years,
        )

        with utils.write_page(args.directory,
                              f'{year}.html',
                              overwrite_ok=args.overwrite) as f:
            f.write(output)

        logger.info('generated %s', f'{year}.html')
