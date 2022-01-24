import unittest

from blog import html


class TestHtml(unittest.TestCase):
    def test_build_page_head(self):
        actual = html.build_page_head(page_filename='test.html',
                                      page_title='Test Page',
                                      page_description='This is a test page.',
                                      page_banner_url='/images/picture.jpg')
        actual = html.stringify_xml(actual)
        expected = '''
<head>
  <title>Test Page</title>
  <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico">
  <link href="./assets/site.css" rel="stylesheet">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="twitter:title" content="Test Page">
  <meta name="twitter:description" content="This is a test page.">
  <meta name="image" content="/images/picture.jpg">
  <meta property="og:url" content="/test.html">
  <meta property="og:type" content="article">
  <meta property="og:title" content="Test Page">
  <meta property="og:description" content="This is a test page.">
  <meta property="og:image" content="/images/picture.jpg">
</head>
'''.strip()
        self.maxDiff = None

        self.assertEqual(actual, expected)

        actual = html.build_page_head(page_filename='test.html',
                                      page_title='Test Page',
                                      page_description='This is a test page.')
        actual = html.stringify_xml(actual)
        expected = '''
<head>
  <title>Test Page</title>
  <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico">
  <link href="./assets/site.css" rel="stylesheet">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="twitter:title" content="Test Page">
  <meta name="twitter:description" content="This is a test page.">
  <meta property="og:url" content="/test.html">
  <meta property="og:type" content="article">
  <meta property="og:title" content="Test Page">
  <meta property="og:description" content="This is a test page.">
</head>
'''.strip()

        self.assertEqual(actual, expected)

    def test_build_site_nav(self):
        actual = html.build_site_nav(filename='index.html',
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

        actual = html.build_site_nav(filename='b.html',
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

    def test_build_page_article(self):
        actual = html.build_page_article('<!-- test -->')
        actual = html.stringify_xml(actual)
        expected = '''
<article>
  <!-- test -->
</article>
'''.strip()

        self.assertEqual(actual, expected)

    def test_build_page_pagination(self):
        actual = html.build_page_pagination(next_page='next.html',
                                            previous_page='previous.html')
        actual = html.stringify_xml(actual)
        expected = '''
<nav class="clearfix">
  <a class="float-left" href="./next.html">⟵ next.html</a>
  <a class="float-right" href="./previous.html">previous.html ⟶</a>
</nav>
'''.strip()

        self.assertEqual(actual, expected)

        actual = html.build_page_pagination(previous_page='previous.html')
        actual = html.stringify_xml(actual)
        expected = '''
<nav class="clearfix">
  <a class="float-right" href="./previous.html">previous.html ⟶</a>
</nav>
'''.strip()

        self.assertEqual(actual, expected)

        actual = html.build_page_pagination(next_page='next.html')
        actual = html.stringify_xml(actual)
        expected = '''
<nav class="clearfix">
  <a class="float-left" href="./next.html">⟵ next.html</a>
</nav>
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

    def test_build_link_table(self):
        with self.assertRaises(ValueError):
            html.build_link_table(rows=[[1], [1, 2]])

        with self.assertRaises(ValueError):
            html.build_link_table(rows=[[1], [2], [3]], header=[1, 2])

        actual = html.build_link_table(rows=[['/a.html', 'The Letter A'],
                                             ['/b.html', 'The Letter B']],
                                       header=['Page', 'Description'])
        actual = html.stringify_xml(actual)
        expected = '''
<table>
  <tr>
    <th>Page</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>
      <a href="/a.html">a.html</a>
    </td>
    <td>The Letter A</td>
  </tr>
  <tr>
    <td>
      <a href="/b.html">b.html</a>
    </td>
    <td>The Letter B</td>
  </tr>
</table>
'''.strip()
        self.assertEqual(actual, expected)
