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
            year=1969,
            author='Dick Butkus')

        expected = '''
<!doctype html>
<html lang="en">

<head>
  <title>Test</title>
  <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico"/>
  <link href="./assets/site.css" rel="stylesheet"/>

  <!-- meta -->
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

  <!-- header -->
  <header>
    <h1>Test</h1>
    <h2>A Test Page</h2>
  </header>

  <hr/>

  <!-- nav -->
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

  <!-- banner -->
  <figure>
    <a href="./images/banners/test.jpg">
      <img alt="banner" src="./images/banners/test.jpg">
    </a>
  </figure>

  <!-- article -->
  <article>

Some content
  </article>

  <hr/>

  <!-- footer -->
  <footer>
    <small>Built with Python 3.9.5</small>
    <small>© Copyright 1969 Dick Butkus</small>
  </footer>

</body>

<!-- No JavaScript, cookies, or tracking.  Just enjoy the reading! -->
</html>
'''.lstrip()

        self.maxDiff = None
        self.assertEqual(actual, expected)
