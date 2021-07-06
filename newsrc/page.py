import functools
import glob
import os

from .config import config
from .files import join, target
from .metadata import parse_metadata
from .files import join
from .logger import logger as l


def files():
    return list(sorted(glob.glob(join('pages/*.*'))))


class BannerMixin(object):
    @property
    def banner_context(self):
        if self.banner_filename:
            return {
                'banner_full_url': self.banner_full_url,
                'banner_relative_url': self.banner_relative_url,
            }
        else:
            return {}

    @property
    def banner_filename(self):
        return self.metadata.get('banner')

    @property
    def banner_relative_url(self):
        if self.banner_filename:
            return f'/images/banners/{banner_filename}'

    @property
    def banner_full_url(self):
        if self.banner_filename:
            base = 'https://www.alexrecker.com'
            return f'{base}/images/banners/{banner_filename}'


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
        l.info(f'building {self} -> {self.relative_target}')

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

    @functools.cached_property
    def context(self):
        twitter = config('twitter')

        return {
            'title': self.title,
            'description': self.description,
            'twitter_handle': twitter['handle'],
        } | self.banner_context


def pages():
    return list(map(Page, files()))
