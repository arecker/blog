"""generate journal archives"""
import random
import logging

from .. import utils, html
from .pages import Page, build_nav_list

logger = logging.getLogger(__name__)


class Archive:
    def __init__(self, site=None, entries=[], full_url=''):
        self.site = site
        self.entries = entries

        if full_url:
            self.protocol = full_url.scheme
            self.domain = full_url.netloc

    def __repr__(self):
        path = utils.prettify_path(utils.ROOT_DIR / 'entries/')
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
            rows = [[f'./{e.filename}', e.description]
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
    # TODO: remove once Site is gone
    from ..models import Site
    site = Site(**vars(args))

    archive = Archive(site=site, entries=site.entries, full_url=args.full_url)
    pages = list(archive.pages())
    total = len(pages)
    nav_pages = build_nav_list()
    for i, page in enumerate(pages):
        page.build(author=args.author,
                   year=args.year,
                   full_url=args.full_url,
                   nav_pages=nav_pages)
        logger.info('generated archive page %s (%d/%d)', page, i + 1, total)
