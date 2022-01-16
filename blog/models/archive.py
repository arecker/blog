import random

from blog import utils, html
from blog.models.page import Page


class Archive:
    def __init__(self, site=None):
        self.site = site

    def __repr__(self):
        path = utils.prettify_path(self.site.directory + '/entries/')
        return f'<Archive {path}>'

    def list_years(self):
        years = [entry.date.year for entry in self.site.entries]
        return sorted(set(years), reverse=True)

    def list_entries(self, year='', month=''):
        entries = (e for e in self.site.entries)
        if year:
            entries = filter(lambda e: year == e.date.year, entries)
        if month:
            entries = filter(lambda e: month == e.date.month, entries)
        return sorted(entries, key=lambda e: e.date, reverse=True)

    def pages(self):
        for year in self.list_years():
            yield Page(filename=f'{year}.html',
                       title=str(year),
                       description=f'All Entries from {year}',
                       banner=self.pick_banner(year=year),
                       is_entry=False,
                       content=self.build_year_page_content(year),
                       site=self.site)

    @property
    def page_names(self):
        return [f'{year}.html' for year in self.list_years()]

    def build_year_page_content(self, year):
        rows = [(e.href, e.description) for e in self.list_entries(year=year)]
        content = html.build_link_table(rows=rows)
        return html.stringify_xml(content)

    def pick_banner(self, year=''):
        entries = self.list_entries(year=year)
        choices = filter(None, (e.banner for e in entries))
        try:
            return random.choice(list(choices))
        except IndexError:
            return None
