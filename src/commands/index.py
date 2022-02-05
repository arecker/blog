"""generate the site homepage"""

import datetime
import logging
import re

from .. import html, utils, git
from .pages import Page, build_nav_list
from .entries import Entry

logger = logging.getLogger(__name__)


class Index(Page):
    filename = 'index.html'

    # TODO: move these to a config
    title = 'Dear Journal'
    description = 'Daily, public journal by Alex Recker'

    def read(self):
        row = html.row()
        latest = self.fetch_latest_entry()
        column = self.html_latest_post(
            title=latest.title,
            description=latest.description,
            page_href=f'./{latest.filename}',
            banner_href=latest.banner_href()
        )
        row.append(column)

        commit = git.get_head_commit()
        column = self.html_last_updated(commit=commit, timestamp=self.make_timestamp())
        row.append(column)
        
        row = html.stringify_xml(row)
        row = self.fix_self_closing_tags(row)
        return row

    def html_latest_post(self, title='', description='', page_href='', banner_href=''):
        """Render latest post column.

        >>> kwargs = {'title': 'Test', 'description': 'a test'}
        >>> kwargs.update({'page_href': 'test.html', 'banner_href': 'test.jpg'})
        >>> print(html.stringify_xml(Index().html_latest_post(**kwargs)))
        <div class="column">
          <h2>Latest Post</h2>
          <a href="test.html">
            <h3 class="title">Test</h3>
          </a>
          <figure>
            <a href="test.html">
              <img src="test.jpg">
            </a>
            <figcaption>
              <p>a test</p>
            </figcaption>
          </figure>
        </div>
        """
        column = html.column()
        column.append(html.h2(text='Latest Post'))

        column.append(
            html.link(href=page_href, children=[html.h3(_class='title', text=title)]))

        if banner_href:
            column.append(
                html.figure(src=banner_href,
                            href=page_href,
                            caption=description))
        else:
            column.append(html.p(text=description))

        return column

    def html_last_updated(self, commit=None, timestamp=None):
        """Render last update column.

        >>> commit = git.Commit(short_hash='abc', long_hash='abcdefg', summary='Fake Commit', url='git.biz/abcdefg')
        >>> timestamp = 'Friday, February 04 2022 9:18 AM CST'
        >>> xml = Index().html_last_updated(commit=commit, timestamp=timestamp)
        >>> print(html.stringify_xml(xml))
        <div class="column">
          <h2>Last Updated</h2>
          <p>
            <small class="code">[<a href="git.biz/abcdefg">abc</a>]<br>Fake Commit</small>
            <br>
            <small>Friday, February 04 2022 9:18 AM CST</small>
          </p>
        </div>
        """
        column = html.column()
        column.append(html.h2(text='Last Updated'))
        column.append(html.p(children=[
            html.small(_class='code', children=[
                '[',
                html.link(href=commit.url, text=commit.short_hash),
                ']',
                html.br(),
                commit.summary,
            ]),
            html.br(),
            html.small(text=timestamp),
        ]))
        
        return column

    def make_timestamp(self):
        timestamp = datetime.datetime.now()
        timestamp_format = '%A, %B %d %Y %-I:%M %p'
        if zone := timestamp.tzname():
            timestamp_format += f' {zone}'
        else:
            timestamp_format += ' CST'

        return timestamp.strftime(timestamp_format)

    def fix_self_closing_tags(self, html: str):
        """Adds extra slash to self-closing tags.

        Unfortunately this is needed to satisfy the XML library's
        parser while reading data.

        >>> html = '<div><img src="bleh.jpg"></div>'
        >>> Index().fix_self_closing_tags(html)
        '<div><img src="bleh.jpg"/></div>'
        """
        p_img = re.compile(r'\<img src=\"(.*)\"\>')
        html =  p_img.sub(r'<img src="\1"/>', html)

        p_br = re.compile(r'\<br\>')
        html =  p_br.sub('<br/>', html)
        return html

    def fetch_latest_entry(self):
        """Return latest journal entry."""

        entries = utils.ROOT_DIR.glob('entries/*.html')
        entries = sorted(entries, reverse=True)
        latest = Entry(source=entries[0])

        # TODO: this is kind of gross, innit?  But we don't need the
        # pagination just to display the latest entry on the homepage,
        # so stub it out.
        latest.paginate()

        return latest


def main(args):
    index = Index()
    nav_pages = build_nav_list()
    index.build(author=args.author,
                year=args.year,
                full_url=args.full_url,
                nav_pages=nav_pages,
                expand_macros=False)
    logger.info('generated index page %s', index)
