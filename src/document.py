import datetime
import pathlib
import string
import xml.etree.ElementTree


class Document:
    def __init__(
            self,
            author='',
            banner_filename='',
            banner_url='',
            content='',
            description='',
            filename='',
            nav_pages=[],
            page_next=None,
            page_previous=None,
            title='',
            url='',
            year=datetime.datetime.now().year,
        ):
        self.author = author
        self.banner_filename = banner_filename
        self.banner_url = banner_url
        self.content = content
        self.description = description
        self.filename = filename
        self.nav_pages = nav_pages
        self.page_next = page_next
        self.page_previous = page_previous
        self.title = title
        self.url = url
        self.year = year

    @property
    def target(self) -> str:
        """Absolute path to the target file"""

        here = pathlib.Path(__file__).parent.absolute()
        root = here.parent
        webroot = root / 'www'

        assert self.filename, "Can't render target unless filename is set!"
        return str(webroot / self.filename)
        

    def render(self) -> str:
        """Render the document as a string."""

        head = self.render_head()
        body = self.render_body()
        
        output = f"""
<html lang="en">
{head}
{body}
</html>
""".strip()

        output = prettify_html(output)

        return f"<!doctype html>\n{output}"

    def render_head(self) -> str:
        """Render document <head>"""

        template = """
<head>
  <title>${title}</title>
  <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico"/>
  <link href="./assets/site.css" rel="stylesheet"/>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="twitter:title" content="${title}"/>
  <meta name="twitter:description" content="${description}"/>
  <meta property="og:url" content="${url}"/>
  <meta property="og:type" content="article"/>
  <meta property="og:title" content="${title}"/>
  <meta property="og:description" content="${description}"/>
  <meta name="image" content="${banner_url}"/>
  <meta property="og:image" content="${banner_url}"/>
</head>
""".strip()

        template = string.Template(template)
        return template.substitute(
            title=self.title, description=self.description,
            url=self.url, banner_url=self.banner_url,
        )



    def render_body(self) -> str:
        """Render document <body>"""

        body = f"""
{self.render_body_header()}
<hr/>
{self.render_body_nav()}
<hr/>
{self.render_body_banner()}
{self.render_body_article()}
<hr/>
{self.render_body_footer()}
""".strip()

        body = '\n'.join(['  ' + line for line in body.splitlines()])
        body = '<body>\n' + body + '\n</body>'
        return body

    def render_body_header(self):
        return f"""
<header>
  <h1>{self.title}</h1>
  <h2>{self.description}</h2>
</header>
""".strip()

    def render_body_nav(self):
        """Render page nav bar"""

        breadcrumbs = f'  <a href="./{self.filename}">{self.filename}</a>'

        if self.filename != 'index.html':
            breadcrumbs += '\n  <span>/</span>'
            breadcrumbs += '\n  <span>{self.filename}</span>'

        navlist = '\n'.join([f'  <a href="./{f}">{f}</a>' for f in self.nav_pages])

        return f"""
<nav>
{breadcrumbs}
<br class="show-on-mobile" />
<span class="float-right-on-desktop">
{navlist}
</span>
</nav>
""".strip()

    def render_body_banner(self) -> str:
        """Render page banner (if one was given)."""

        if not self.banner_filename:
            return ""

        return f"""
<figure>
  <a href="./{self.banner_filename}">
    <img alt="banner" src="./{self.banner_filename}">
  </a>
</figure>
""".strip()

    def render_body_article(self) -> str:
        """Render page <article>.

        Returns Document().content if it's set, otherwise will try to
        build it dynamically from rows and columns.
        """
        if self.content:
            content = self.content
        else:
            # TODO: Render from rows, columns, and objects?
            content = ''

        pages = []
        if self.page_previous:
            pages.append(f'  <a class="float-left" href="./{self.page_previous}">⟵ {self.page_previous}</a>')
        if self.page_next:
            pages.append(f'  <a class="float-right" href="./{self.page_next}">{self.page_next} ⟶</a>')

        if pages:
            content += '\n<nav class="clearfix">\n' + '\n'.join(pages) + '\n</nav>'

        return f'<article>\n{content}\n</article>'

    def render_body_footer(self) -> str:
        """Render page <footer>"""

        return f"""
<footer>
  <small>© Copyright {self.year} {self.author}</small>
</footer>
""".strip()


def prettify_html(html: str) -> str:
    """Prettify an HTML string."""

    # Need to use a custom target so we read comments too.
    target = xml.etree.ElementTree.TreeBuilder(insert_comments=True)
    parser = xml.etree.ElementTree.XMLParser(target=target)

    try:
        parser.feed(html)
        html = parser.close()
        xml.etree.ElementTree.indent(html)
        return xml.etree.ElementTree.tostring(html, encoding='unicode', method='html')
    except xml.etree.ElementTree.ParseError as e:
        raise ValueError(f'{e}\n---\n{html}\n---')
