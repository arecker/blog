from src import utils


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
