import unittest

from src import html


class TestHtml(unittest.TestCase):
    def test_build_page_nav(self):
        actual = html.build_page_nav(filename='index.html',
                                     nav_pages=['a.html', 'b.html'])
        actual = html.stringify_xml(actual)
        expected = '''
 <nav>
  <a href="/">index.html</a>
  <br class="show-on-mobile">
  <span class="float-right-on-desktop">
    <a href="/a.html">a.html</a>
    <a href="/b.html">b.html</a>
  </span>
</nav>'''.strip()

        self.assertEqual(actual, expected)

        actual = html.build_page_nav(filename='b.html',
                                     nav_pages=['a.html', 'b.html'])
        actual = html.stringify_xml(actual)
        expected = '''
 <nav>
  <a href="/">index.html</a>
  <span>/</span>
  <span>b.html</span>
  <br class="show-on-mobile">
  <span class="float-right-on-desktop">
    <a href="/a.html">a.html</a>
    <a href="/b.html">b.html</a>
  </span>
</nav>'''.strip()

        self.assertEqual(actual, expected)

    def test_build_page_header(self):
        actual = html.build_page_header(title='Test Page',
                                        description='This is a test page.')
        actual = html.stringify_xml(actual)
        expected = '''
<header>
  <h1>Test Page</h1>
  <h2>This is a test page.</h2>
</header>'''.strip()

        self.assertEqual(actual, expected)

    def test_build_page_banner(self):
        actual = html.build_page_banner(banner_url='/images/me.jpg')
        actual = html.stringify_xml(actual)
        expected = '''
<figure>
  <a href="/images/me.jpg">
    <img alt="banner" src="/images/me.jpg">
  </a>
</figure>
'''.strip()

        self.assertEqual(actual, expected)

    def test_build_page_footer(self):
        actual = html.build_page_footer(author='Steve', year='2000')
        actual = html.stringify_xml(actual)
        expected = '''
<footer>
  <small>© Copyright 2000 Steve</small>
</footer>
'''.strip()

        self.assertEqual(actual, expected)
