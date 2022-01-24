import unittest

from ..models import Page


class TestPage(unittest.TestCase):
    def test_slug(self):
        page = Page(source='some/directory/page.md')
        self.assertEqual(page.slug, 'page')

    def test_filename(self):
        page = Page(source='some/directory/page.md')
        self.assertEqual(page.filename, 'page.html')
