"""Functions for rendering text and manipulating strings."""

from .utils import StringWriter


def slugify(text: str) -> str:
    """Return a slug-friendly version of a string.

    >>> slugify('Some String')
    'some-string'
    """
    text = text.lower()
    text = text.replace(' ', '-')
    return text


def render_index(headings=[], render_heading: callable = None) -> str:
    """Render an HTML index

    >>> print(render_index(['Fruits', 'Vegetables', 'Spices']).strip())
    <ul>
      <li><a href="#fruits">Fruits</a></li>
      <li><a href="#vegetables">Vegetables</a></li>
      <li><a href="#spices">Spices</a></li>
    </ul>

    Use a special callable to render the heading as a list item.

    >>> print(render_index(['My Thing'], render_heading=lambda h: h + ', please...').strip())
    <ul>
      <li><a href="#my-thing">My Thing, please...</a></li>
    </ul>
    """

    render_heading = render_heading or (lambda h: h)
    content = StringWriter()
    items = [(slugify(h), render_heading(h)) for h in headings]
    items = [f'<a href="#{anchor}">{text}</a>' for anchor, text in items]
    content.ul(items=items)
    return content.text
