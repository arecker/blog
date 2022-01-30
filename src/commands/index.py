"""generate the site homepage"""

import logging
import re

from .. import html, utils
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
        row.append(self.html_latest_post())
        row = html.stringify_xml(row)
        row = self.fix_self_closing_tags(row)
        return row

    def html_latest_post(self):
        column = html.column()
        column.append(html.h2(text='Latest Post'))

        latest = self.fetch_latest_entry()
        column.append(
            html.link(href=f'./{latest.filename}',
                      element=html.h3(_class='title', text=latest.title)))

        if image := latest.banner_href():
            column.append(
                html.figure(src=image,
                            href=f'./{latest.filename}',
                            caption=latest.description))
        else:
            column.append(html.p(text=latest.description))

        return column

    def fix_self_closing_tags(self, html: str):
        p = re.compile(r'\<img src=\"(.*)\"\>')
        return p.sub(r'<img src="\1"/>', html)

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
