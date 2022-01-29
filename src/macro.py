"""functions for expanding magic comment macros"""

import datetime
import logging
import re

from . import git

logger = logging.getLogger(__name__)


class Expander:
    r_macro = re.compile(r'(?P<whitespace> *)<!-- blog:(?P<key>\S+) -->',
                         re.MULTILINE)

    def __init__(self, site=None, timestamp=None):
        self.site = site
        self.markup = {}
        self.timestamp = timestamp or datetime.datetime.now()

    def populate(self):
        # timestamp
        timestamp_format = '%A, %B %d %Y %-I:%M %p'
        if zone := self.timestamp.tzname():
            timestamp_format += f' {zone}'
        else:
            timestamp_format += ' CST'

        self.markup['timestamp'] = self.timestamp.strftime(timestamp_format)

        # latest
        if self.site.latest.banner_filename():
            self.markup['latest'] = f'''
<a href="./{self.site.latest.filename}">
  <h3 class="title">{self.site.latest.title}</h3>
</a>
<figure>
  <a href="./{self.site.latest.filename}">
    <img src="{self.site.latest.banner_href()}">
  </a>
  <figcaption>
    <p>{self.site.latest.description}</p>
  </figcaption>
</figure>'''.strip()
        else:
            self.markup['latest'] = f'''
<a href="./{self.site.latest.filename}">
  <h3 class="title">{self.site.latest.title}</h3>
</a>
<p>{self.site.latest.description}</p>
'''.strip()

        # commit
        commit = git.get_head_commit()
        self.markup[
            'commit'] = f'[<a href="{commit.url}">{commit.short_hash}</a>]<br/>{commit.summary}'

    def expand(self, html):
        return self.r_macro.sub(self.replace, html)

    def replace(self, match):
        whitespace, key = match.groups()
        expansion = self.markup[key]
        expansion = '\n'.join(
            [whitespace + line for line in expansion.splitlines()])
        return expansion
