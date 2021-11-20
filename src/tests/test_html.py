import unittest

from src import html


class TestHtml(unittest.TestCase):
    def test_build_nav(self):
        actual = html.build_nav(pages=['a.html', 'b.html'])
        actual = html.stringify_xml(actual)
        expected = '''
<nav>
  <a href="/a.html">a.html</a>
  <a href="/b.html">b.html</a>
</nav>
'''.strip()

        self.assertEqual(actual, expected)

    def test_build_page_header(self):
        actual = html.build_page_header(title='Test Page',
                                        description='This is a test page.')
        actual = html.stringify_xml(actual)
        expected = '''
<header>
  <h1>Test Page</h1>
  <h2>This is a test page.</h2>
</header>
'''.strip()

        self.assertEqual(actual, expected)
