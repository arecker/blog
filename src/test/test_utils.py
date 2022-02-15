import unittest
import urllib.parse

from .. import utils


class TestStringWriter(unittest.TestCase):
    def test_wrapper(self):
        w = utils.StringWriter()
        with w.block('test', c='2', a='1', _class='center'):
            w.write('testing')

        expected = '''
<test a="1" c="2" class="center">
  testing
</test>
'''.lstrip()

        self.assertEqual(w.text, expected)


class TestMetadataParseHTML(unittest.TestCase):
    def test_one(self):
        actual = utils.metadata_parse_html('''
<!-- meta:title party, dumplings, and blogging -->
''')
        expected = {'title': 'party, dumplings, and blogging'}
        self.assertDictEqual(actual, expected)

    def test_two(self):
        actual = utils.metadata_parse_html('''
<!-- just a regular comment! -->
<!-- meta:title rodney stories, karta's enclosure, and ollie's championship -->
<!-- meta:banner 2022-02-14.jpg -->

<h2>Hello there!</h2>
''')
        expected = {
            'title':
            'rodney stories, karta\'s enclosure, and ollie\'s championship',
            'banner': '2022-02-14.jpg'
        }
        self.assertDictEqual(actual, expected)


class TestPaginateList(unittest.TestCase):
    def test_one(self):
        result = utils.paginate_list(['a', 'b', 'c'])
        self.assertIsNone(result['a'].previous)
        self.assertEqual(result['a'].next, 'b')
        self.assertEqual(result['c'].previous, 'b')
        self.assertIsNone(result['c'].next)


class TestRenderPage(unittest.TestCase):
    def test_page(self):
        page = utils.Page(filename='test.html',
                          title='Test',
                          description='A Test Page',
                          banner='test.jpg')

        actual = utils.render_page(
            page,
            full_url=urllib.parse.urlparse('http://localhost:8000'),
            content='Some content',
            nav_pages=['a.html', 'b.html'],
            copyright_year=1969,
            python_version='1.2.3',
            author='Dick Butkus')

        expected = '''
<!doctype html>
<html lang="en">

<head>
  <title>Test</title>

  <!-- Page Assets -->
  <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico"/>
  <link href="./assets/site.css" rel="stylesheet"/>

  <!-- Page Metadata -->
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="twitter:title" content="Test"/>
  <meta name="twitter:description" content="A Test Page"/>
  <meta property="og:url" content="http://localhost:8000/test.html"/>
  <meta property="og:type" content="article"/>
  <meta property="og:title" content="Test"/>
  <meta property="og:description" content="A Test Page"/>
  <meta name="image" content="http://localhost:8000/images/banners/test.jpg"/>
  <meta property="og:image" content="http://localhost:8000/images/banners/test.jpg"/>

</head>

<body>

  <!-- Page Header -->
  <header>
    <h1>Test</h1>
    <h2>A Test Page</h2>
  </header>

  <hr/>

  <!-- Site Navigation -->
  <nav>
    <a href="./index.html">index.html</a>
    <span>/</span>
    <span>test.html</span>
    <br class="show-on-mobile">
    <span class="float-right-on-desktop">
      <a href="./a.html">a.html</a>
      <a href="./b.html">b.html</a>
    </span>
  </nav>

  <hr/>

  <!-- Page Banner -->
  <figure>
    <a href="./images/banners/test.jpg">
      <img src="./images/banners/test.jpg" alt="banner" />
    </a>
  </figure>

  <!-- Page Content -->
  <article>

Some content
  </article>

  <hr/>

  <!-- Page Footer -->
  <footer>
    <small>Built with Python 1.2.3</small>
    <small>© Copyright 1969 Dick Butkus</small>
  </footer>

</body>

<!-- No JavaScript, cookies, or tracking.  Just enjoy the reading! -->
</html>
'''.lstrip()

        self.maxDiff = None
        self.assertEqual(actual, expected)
