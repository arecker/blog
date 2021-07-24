import re


def extract_markdown_frontmatter(content: str) -> dict:
    r"""Extracts YAML frontmatter from a string, returning a dict form
    along with the rest of the string.

    >>> content = '---\na: 1\nb: 2\nc: do re mi\n---\nThis is a test.'
    >>> results = extract_markdown_frontmatter(content)
    >>> results[0]
    {'a': '1', 'b': '2', 'c': 'do re mi'}
    >>> results[1]
    'This is a test.'
    """

    r_frontmatter = re.compile(r'^---\n(.*?)\n---\n(.*)$', re.DOTALL)
    r_frontmatter_line = re.compile(r'^(?P<key>.*?):\W?(?P<value>.*)$',
                                    re.MULTILINE)

    if match := r_frontmatter.match(content):
        body, rest = match.group(1, 2)
        data = dict(r_frontmatter_line.findall(body))
        return data, rest

    return None, content
