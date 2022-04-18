import unittest
import unittest.mock
import xml.etree.ElementTree

from ..render import Renderer, render_page


class TestRenderer(unittest.TestCase):
    def test_write(self):
        r = Renderer()
        self.assertEqual(r.text, '')

        r.write('First line')
        self.assertEqual(r.text, 'First line\n')

        r.write('Second line')
        self.assertEqual(r.text, 'First line\nSecond line\n')

        r.text = ''
        r.write('no newline!', add_newline=False)
        self.assertEqual(r.text, 'no newline!')

        r.text = ''
        r.current_indent_level = 2
        r.write('First')

        r.current_indent_level = 4
        r.write('Second')

        r.current_indent_level = 0
        r.write('Third')
        self.assertEqual(r.text, '  First\n    Second\nThird\n')

    def test_indent(self):
        r = Renderer()

        r.write('Unindented.')

        with r.indent(2):
            r.write('Indented!')

        r.write('Unindented.')

        self.assertEqual(r.text, 'Unindented.\n  Indented!\nUnindented.\n')

    def test_block(self):
        r = Renderer()
        r.block('p', contents='This is a paragraph.')
        self.assertEqual(r.text.strip(), '<p>This is a paragraph.</p>')

        r = Renderer()
        r.block('p', 'Unsafe characters, like "&", "<", and ">"')
        self.assertEqual(
            r.text.strip(), '<p>Unsafe characters, like '
            '&quot;&amp;&quot;, '
            '&quot;&lt;&quot;, and '
            '&quot;&gt;&quot;</p>')

        r = Renderer()
        r.block('div',
                _id='some-id',
                _class='some-class',
                width=400,
                contents='')
        self.assertEqual(
            r.text, '''
<div class="some-class" id="some-id" width="400"></div>
'''.lstrip())

        r = Renderer()
        r.block('img', src='blah.jpg', alt='hello', self_closing=True)
        self.assertEqual(r.text.strip(), '<img alt="hello" src="blah.jpg" />')

        r = Renderer()
        with self.assertRaisesRegex(AssertionError,
                                    'contents in a self-closing tag'):
            r.block('a', contents='bleh', self_closing=True)

    def test_wrapping_block(self):
        r = Renderer()
        with r.wrapping_block('a'):
            r.block('b', 'nested!')
        self.assertEqual(r.text, '''
<a>
  <b>nested!</b>
</a>
'''.lstrip())
        r = Renderer()
        with r.wrapping_block('div', _id='some-id', _class='some-class'):
            r.block('p', 'nested!')
        self.assertEqual(
            r.text, '''
<div class="some-class" id="some-id">
  <p>nested!</p>
</div>
'''.lstrip())

    def test_comment(self):
        r = Renderer()
        r.comment('A comment')
        self.assertEqual(r.text, '<!-- A comment -->\n')

    def test_newline(self):
        r = Renderer()
        r.write('hello')
        r.newline()
        r.write('hello again')
        self.assertEqual(r.text, 'hello\n\nhello again\n')

    def test_header(self):
        r = Renderer(starting_indent_level=4)
        r.header('Test page', 'Just a test page!')
        self.assertEqual(
            r.text, '''    <header>
      <h1>Test page</h1>
      <p>Just a test page!</p>
    </header>
''')

    def test_breadcrumbs(self):
        r = Renderer()
        r.breadcrumbs(filename='index.html')
        self.assertEqual(
            r.text.strip(), '''
<nav>
  <a href="./index.html">index.html</a>
</nav>
'''.strip())

        r = Renderer()
        r.breadcrumbs(filename='some-page.html')
        self.assertEqual(
            r.text.strip(), '''
<nav>
  <a href="./index.html">index.html</a>
  <span>/ some-page.html</span>
</nav>
'''.strip())

    def test_figure(self):
        r = Renderer()

        with self.assertRaisesRegex(AssertionError, 'should have an alt'):
            r.figure(src='test.jpg')

        with self.assertRaisesRegex(AssertionError, 'should have an src'):
            r.figure(alt='test')

        r.figure(src='test.jpg', alt='a test image')
        self.assertEqual(
            r.text.strip(), '''
<figure>
  <a href="test.jpg">
    <img alt="a test image" src="test.jpg" />
  </a>
</figure>'''.strip())

        r = Renderer()
        r.figure(src='test.jpg', alt='a test image', href="google.com")
        self.assertEqual(
            r.text.strip(), '''
<figure>
  <a href="google.com">
    <img alt="a test image" src="test.jpg" />
  </a>
</figure>'''.strip())
        r = Renderer()
        r.figure(src='test.jpg', alt='a test image', caption="a test caption!")
        self.assertEqual(
            r.text.strip(), '''
<figure>
  <a href="test.jpg">
    <img alt="a test image" src="test.jpg" />
  </a>
  <figcaption>
    <p>a test caption!</p>
  </figcaption>
</figure>'''.strip())

    def test_hr(self):
        r = Renderer()
        r.hr()
        self.assertEqual(r.text.strip(), '<hr />')

    def test_meta(self):
        r = Renderer()
        r.meta(charset='UTF-8')
        self.assertEqual(r.text.strip(), '<meta charset="UTF-8" />')

        r = Renderer()
        r.meta(_property='og:url')
        self.assertEqual(r.text.strip(), '<meta property="og:url" />')

    def test_link(self):
        r = Renderer()
        r.link(href='./assets/site.css', rel='stylesheet')
        self.assertEqual(r.text.strip(),
                         '<link href="./assets/site.css" rel="stylesheet" />')

    def test_footer(self):
        r = Renderer()
        r.footer(author='Austin Powers', year=1969)
        self.assertEqual(
            r.text.strip(), '''
<footer>
  <small>© Copyright 1969 Austin Powers</small>
</footer>
'''.strip())

    def test_as_html(self):
        r = Renderer()
        with r.wrapping_block('body'):
            r.block('p', contents='This is a little test.')
        result = r.as_html()
        self.assertEqual(
            result, '''
<!doctype html>
<html lang="en">

<body>
  <p>This is a little test.</p>
</body>

</html>
'''.lstrip())

    def test_as_xml(self):
        r = Renderer()
        r.write('not even close to valid XML!')
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            r.as_xml()

        r = Renderer()
        with r.wrapping_block('feed', xmlns='http://www.w3.org/2005/Atom'):
            r.write('''
  <title>Dear Journal</title>
  <subtitle>Daily, public journal by Alex Recker</subtitle>
  <author>
    <name>Alex Recker</name>
    <email>alex@reckerfamily.com</email>
  </author>'''.strip())

        self.assertEqual(
            r.as_xml(), '''
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Dear Journal</title>
  <subtitle>Daily, public journal by Alex Recker</subtitle>
  <author>
    <name>Alex Recker</name>
    <email>alex@reckerfamily.com</email>
  </author>
</feed>
'''.lstrip())


class TestRender(unittest.TestCase):
    maxDiff = None

    def test_render_page(self):
        page = unittest.mock.Mock(
            title='Some Test Page',
            description='Just a test page for the test suite',
            filename='test.html',
            banner='test.jpg')

        content = '''    <p>This is some test conent.</p>

    <figure>
      <a href="test.jpg">
        <img src="test.jpg" alt="test"/>
      </a>
    </figure>'''

        actual = render_page(page, content=content, full_url='http://localhost:8080', year=1990, author='Joe Schmo')
        expected = '''
<!doctype html>
<html lang="en">

<head>
  <title>Some Test Page</title>

  <!-- Page Assets -->
  <link href="./favicon.ico" rel="shortcut icon" type="image/x-icon" />
  <link href="./assets/site.css" rel="stylesheet" />

  <!-- Page Metadata -->
  <meta charset="UTF-8" />
  <meta content="width=device-width, initial-scale=1" name="viewport" />
  <meta content="Some Test Page" name="twitter:title" />
  <meta content="Just a test page for the test suite" name="twitter:description" />
  <meta content="http://localhost:8080/test.html" name="og:url" />
  <meta content="article" property="og:type" />
  <meta content="Some Test Page" property="og:title" />
  <meta content="Just a test page for the test suite" property="og:description" />

</head>

<body>
  <article>

    <!-- Page Header -->
    <header>
      <h1>Some Test Page</h1>
      <p>Just a test page for the test suite</p>
    </header>

    <hr />

    <!-- Page Breadcrumbs -->
    <nav>
      <a href="./index.html">index.html</a>
      <span>/ test.html</span>
    </nav>

    <hr />

    <!-- Page Banner -->
    <figure>
      <a href="./images/banners/test.jpg">
        <img alt="page banner" src="./images/banners/test.jpg" />
      </a>
    </figure>

    <!-- Begin Page Content -->
    <p>This is some test conent.</p>

    <figure>
      <a href="test.jpg">
        <img src="test.jpg" alt="test"/>
      </a>
    </figure>
    <!-- End Page Content -->

  </article>

  <hr />

  <!-- Page Footer -->
  <footer>
    <small>© Copyright 1990 Joe Schmo</small>
  </footer>

</body>

</html>
'''.lstrip()
        self.assertEqual(actual, expected)
