"""generate journal archives"""
import random
import logging
import pathlib

from blog import utils, html
from blog.models import Page, Site

logger = logging.getLogger(__name__)
here = pathlib.Path(__file__).parent


class Archive:
    def __init__(self, site=None, entries=[], protocol='', domain=''):
        self.site = site
        self.entries = entries
        self.protocol = protocol
        self.domain = domain

    def __repr__(self):
        path = utils.prettify_path(here.parent.parent / 'entries/')
        return f'<Archive {path}>'

    def list_years(self):
        years = [entry.date.year for entry in self.entries]
        return sorted(set(years), reverse=True)

    def list_entries(self, year='', month=''):
        entries = (e for e in self.entries)
        if year:
            entries = filter(lambda e: year == e.date.year, entries)
        if month:
            entries = filter(lambda e: month == e.date.month, entries)
        return sorted(entries, key=lambda e: e.date, reverse=True)

    def pages(self):
        years = self.list_years()
        yield Page(filename='entries.html',
                   title='Entries',
                   description='Complete Archive of Journal Entries',
                   banner=self.pick_banner(),
                   is_entry=False,
                   content=self.build_page_content(year=None, years=years),
                   site=self.site)

        for year in years:
            yield Page(filename=f'{year}.html',
                       title=str(year),
                       description=f'All Entries from {year}',
                       banner=self.pick_banner(year=year),
                       is_entry=False,
                       content=self.build_page_content(year=year, years=years),
                       site=self.site)

    def build_page_content(self, year=None, years=[]):
        root = html.p()
        nav_pages = [f'{y}.html' for y in years]
        nav = html._nav()
        nav.append(html.build_page_nav(nav_pages=nav_pages))
        root.append(nav)
        content = html.stringify_xml(root)

        if year:
            rows = [[e.href(), e.description]
                    for e in self.list_entries(year=year)]
            table = html.build_link_table(rows=rows)
            table = html.stringify_xml(table)
            content = content + '\n' + table

        content = f'''
<p>
  <span>
    <a href="https://validator.w3.org/feed/check.cgi?url={self.protocol}%3A//{self.domain}/feed.xml">
      <img src="/assets/valid-atom.png" alt="[Valid Atom 1.0]" title="Validate my Atom 1.0 feed" />
    </a>
  </span>
  <br/>
  RSS feed available here: <a href="/feed.xml">feed.xml</a>
</p>
'''.strip() + '\n' + content

        return content

    def pick_banner(self, year=''):
        entries = self.list_entries(year=year)
        choices = filter(None, (e.banner for e in entries))
        try:
            return random.choice(list(choices))
        except IndexError:
            return None


def main(args):
    site = Site(**vars(args))
    archive = Archive(site=site,
                      entries=site.entries,
                      protocol=args.protocol,
                      domain=args.domain)
    pages = list(archive.pages())
    total = len(pages)
    for i, page in enumerate(pages):
        page.build(author=args.author)
        logger.info('generated archive page %s (%d/%d)', page, i + 1, total)
