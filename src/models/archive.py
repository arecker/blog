from src import utils, html
from src.models.page import Page


class Archive:
    def __init__(self, site=None):
        self.site = site

    def __repr__(self):
        path = utils.prettify_path(self.site.directory + '/entries/')
        return f'<Archive {path}>'

    def list_years(self):
        years = [entry.date.year for entry in self.site.entries]
        return sorted(set(years), reverse=True)

    def list_months(self, year):
        entries = filter(lambda e: year == e.date.year, self.site.entries)
        months = [e.date.month for e in entries]
        return sorted(set(months), reverse=True)

    def list_entries(self, year, month):
        entries = filter(lambda e: year == e.date.year, self.site.entries)
        entries = filter(lambda e: month == e.date.month, entries)
        return sorted(entries, key=lambda e: e.date, reverse=True)

    @property
    def pages(self):
        for year in self.list_years():
            for month in self.list_months(year):
                yield Page(filename=f'{year}-{month:02}.html')
            yield Page(filename=f'{year}.html')

    def build_year_page(self, year):
        months = self.list_months(year)
        data = [(self.site.href(f'{year}-{m:02}.html'),
                 len(self.list_entries(year, m))) for m in months]
        return data
