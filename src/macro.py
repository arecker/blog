"""functions for expanding magic comment macros"""

import logging
import re

logger = logging.getLogger(__name__)


class Expander:
    r_macro = re.compile(r'(?P<whitespace> *)<!-- blog:(?P<key>\S+) -->',
                         re.MULTILINE)

    def __init__(self, site=None):
        self.site = site
        self.markup = {}

    def populate(self):
        # timestamp
        timestamp_format = '%A, %B %d %Y %-I:%M %p'
        if zone := self.site.timestamp.tzname():
            timestamp_format += f' {zone}'
        else:
            timestamp_format += ' CST'

        self.markup['timestamp'] = self.site.timestamp.strftime(
            timestamp_format)

        # latest
        if self.site.latest.banner:
            self.markup['latest'] = f'''
<a href="/{self.site.latest.filename}">
  <h3 class="title">{self.site.latest.title}</h3>
</a>
<figure>
  <a href="/{self.site.latest.filename}">
    <img src="/images/banners/{self.site.latest.banner}">
  </a>
  <figcaption>
    <p>{self.site.latest.description}</p>
  </figcaption>
</figure>'''.strip()
        else:
            self.markup['latest'] = f'''
<a href="/{self.site.latest.filename}">
  <h3 class="title">{self.site.latest.title}</h3>
</a>
<p>{self.site.latest.description}</p>
'''.strip()

        # commit
        self.markup[
            'commit'] = f'[<a href="{self.site.commit_url}">{self.site.commit.short_hash}</a>]<br/>{self.site.commit.summary}'

        # entries
        # TODO: this is temporary, just to get rid of the old magic
        # comments stuff burried in Document.
        row_fmt = '''
  <tr>
    <td><a href="/{filename}">{filename}</a></td>
    <td>{description}</td>
  </tr>
'''.strip()
        rows = '\n'.join([
            row_fmt.format(filename=e.filename, description=e.description)
            for e in self.site.entries
        ])
        self.markup['entries'] = f'<table>\n  {rows}\n</table>'

    def expand(self, html):
        return self.r_macro.sub(self.replace, html)

    def replace(self, match):
        whitespace, key = match.groups()
        expansion = self.markup[key]
        expansion = '\n'.join(
            [whitespace + line for line in expansion.splitlines()])
        return expansion
