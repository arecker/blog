import datetime
import functools
import glob
import os

from . import partials
from .banner import BannerMixin
from .config import config
from .files import join, target
from .logger import logger
from .metadata import parse_metadata
from .template import render_page


def files():
    return list(sorted(glob.glob(join('pages/*.*'))))


def make_global_context():
    data = {}

    # metadata
    twitter = config('twitter')
    data.update({'twitter_handle': twitter['handle']})

    # nav
    data.update({'partial_nav': partials.nav(pagelist=build_nav_list())})

    # footer
    site = config('site')
    now = datetime.datetime.now().astimezone()
    timestamp = now.strftime('%B %-d %Y, %I:%M %p %Z')
    data.update({
        'partial_footer':
        partials.footer(
            year=now.year,
            author=site['author'],
            timestamp=timestamp,
        )
    })

    return data


class Page(BannerMixin):
    def __init__(self, source):
        self.source = source

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.filename}>'

    @property
    def filename(self):
        base, _ = os.path.splitext(self.source)
        return os.path.basename(base) + '.html'

    @property
    def target(self):
        return target(self.filename)

    @property
    def relative_target(self):
        return f'www/{self.filename}'

    @property
    def permalink(self):
        base, _ = os.path.splitext(self.filename, )
        return f'{base}.html'

    def build(self):
        logger.info(f'building {self} -> {self.relative_target}')

    @functools.cached_property
    def metadata(self):
        with open(self.source) as f:
            data, _ = parse_metadata(f.read(), legacy=True)
        return data

    @property
    def title(self):
        return self.metadata['title']

    @property
    def description(self):
        return self.metadata['description']

    @property
    def content(self):
        with open(self.source) as f:
            return f.read()

    @functools.cached_property
    def context(self):
        data = {}

        # Page metadata
        data.update({
            'content': self.content,
            'description': self.description,
            'permalink': self.filename,
            'title': self.title,
        } | self.banner_context)

        # Page partials
        data.update({
            'partial_breadcrumbs':
            partials.breadcrumbs(permalink=self.permalink),
            'partial_banner':
            partials.banner(filename=self.banner_filename),
            'partial_header':
            partials.header(title=self.title, description=self.description),
            'partial_pagination':
            self.render_pagination()
        })

        return data

    def render_pagination(self):
        return ''

    @property
    def nav_index(self):
        try:
            return self.metadata.get('nav')
        except TypeError:
            return None

    def render(self, global_context={}):
        context = global_context | self.context
        return render_page(**context)


def pages():
    return list(map(Page, files()))


def build_nav_list() -> [str]:
    """
    Retrieve an ordered list of page permalinks that should be in the
    nav.  These are flagged and ordered like so:

    <!-- metadata:nav: 1 -->
    """
    included_pages = [page for page in pages() if page.nav_index]
    sorted_pages = sorted(included_pages, key=lambda p: p.nav_index)

    logger.info('extracted site navigation: %s', sorted_pages)
    return [p.permalink for p in sorted_pages]
