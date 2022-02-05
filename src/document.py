import string


class Document:
    def __init__(self, title='', description='', url='', banner_url=''):
        self.title = title
        self.description = description
        self.url = url
        self.banner_url = banner_url

    def render(self) -> str:
        """Render the document as a string."""

        head = self.render_head()
        body = self.render_body()
        output = """
<!doctype html>
<html lang="en">
${head}
${body}
</html>
""".strip()

        return output

    def render_head(self) -> str:
        """Render document <head>"""

        template = """
<head>
  <title>${title}</title>
  <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico">
  <link href="./assets/site.css" rel="stylesheet">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="twitter:title" content="${title}">
  <meta name="twitter:description" content="${description}">
  <meta property="og:url" content="${url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="${title}">
  <meta property="og:description" content="${description}">
  <meta name="image" content="${banner_url}">
  <meta property="og:image" content="${banner_url}">
</head>
""".strip()

        template = string.Template(template)
        return template.substitute(
            title=self.title, description=self.description,
            url=self.url, banner_url=self.banner_url,
        )



    def render_body(self) -> str:
        """Render document <body>"""

        template = """
  <body>
    <header>
      <h1>Monday, January 3 2022</h1>
      <h2>the ball drop, exercise, and resolutions</h2>
    </header>
    <hr>
    <nav>
      <a href="/">index.html</a>
      <span>/</span>
      <span>2022-01-03.html</span>
      <br class="show-on-mobile">
      <span class="float-right-on-desktop">
        <a href="/entries.html">entries.html</a>
        <a href="/pets.html">pets.html</a>
        <a href="/contact.html">contact.html</a>
      </span>
    </nav>
    <hr>
    <figure>
      <a href="./images/banners/2022-01-03.jpg">
        <img alt="banner" src="./images/banners/2022-01-03.jpg">
      </a>
    </figure>
    <article>
    </article>
    <hr>
    <footer>
      <small>© Copyright 2022 Alex Recker</small>
    </footer>
  </body>
""".strip()
