import unittest

from .. import Document


class TestDocument(unittest.TestCase):
    def test_render_head(self):
        actual = Document(
            title="Test Page",
            description="This is a test page."
        ).render_head()

        expected = """
<head>
  <title>Test Page</title>
  <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico"/>
  <link href="./assets/site.css" rel="stylesheet"/>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="twitter:title" content="Test Page"/>
  <meta name="twitter:description" content="This is a test page."/>
  <meta property="og:url" content=""/>
  <meta property="og:type" content="article"/>
  <meta property="og:title" content="Test Page"/>
  <meta property="og:description" content="This is a test page."/>
  <meta name="image" content=""/>
  <meta property="og:image" content=""/>
</head>
""".strip()
        self.maxDiff = None
        self.assertEqual(actual, expected)

    def test_render_body_header(self):
        actual = Document(
            title="Test Page",
            description="This is a test page."
        ).render_body_header()

        expected = """
<header>
  <h1>Test Page</h1>
  <h2>This is a test page.</h2>
</header>
""".strip()

        self.assertEqual(actual, expected)

    def test_body_nav(self):
        actual = Document(
            filename='test.html',
            nav_pages=['a.html', 'b.html']
        ).render_body_nav()

        expected = """
<nav>
  <a href="./index.html">index.html</a>
  <span>/</span>
  <span>test.html</span>
  <br class="show-on-mobile" />
  <span class="float-right-on-desktop">
    <a href="./a.html">a.html</a>
    <a href="./b.html">b.html</a>
  </span>
</nav>
""".strip()
        

    def test_render_body_banner(self):
        self.assertEqual(Document().render_body_banner(), "")

        actual = Document(banner_filename="test.jpg").render_body_banner()

        expected = """
<figure>
  <a href="./test.jpg">
    <img alt="banner" src="./test.jpg">
  </a>
</figure>
""".strip()

    def test_render_body_article(self):
        actual = Document(content='<p>This is a test.</p>').render_body_article()

        expected = """
<article>
<p>This is a test.</p>
</article>
""".strip()
        
        actual = Document(
            content='<p>This is a test.</p>',
            page_next='next.html',
            page_previous='previous.html',
        ).render_body_article()

        expected = """
<article>
<p>This is a test.</p>
<nav class="clearfix">
  <a class="float-left" href="./previous.html">⟵ previous.html</a>
  <a class="float-right" href="./next.html">next.html ⟶</a>
</nav>
</article>
""".strip()
        
        actual = Document(
            content='<p>This is a test.</p>',
            page_previous='previous.html',
        ).render_body_article()

        expected = """
<article>
<p>This is a test.</p>
<nav class="clearfix">
  <a class="float-left" href="./previous.html">⟵ previous.html</a>
</nav>
</article>
""".strip()

        actual = Document(
            content='<p>This is a test.</p>',
            page_next='next.html',
        ).render_body_article()

        expected = """
<article>
<p>This is a test.</p>
<nav class="clearfix">
  <a class="float-right" href="./next.html">next.html ⟶</a>
</nav>
</article>
""".strip()

    def test_render_body_footer(self):
        actual = Document(author='Dick Butkus', year=1985).render_body_footer()

        expected = """
<footer>
  <small>© Copyright 1985 Dick Butkus</small>
</footer>
""".strip()
