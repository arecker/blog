import string
import re

from newsrc.files import join

page_template_path = join('newsrc/templates/page.html.tmpl')


def render_page(content='', **kwargs):
    with open(page_template_path) as f:
        base_template_content = f.read()

    content = escape_dollar_signs(content)

    full_template_content = base_template_content.replace(
        '<!-- CHILD_CONTENT -->', indent_body(content))

    full_template = string.Template(full_template_content)

    return full_template.substitute(**kwargs)


def escape_dollar_signs(content):
    """
    Safely escapes all regular dollar signs in a string to prepare it
    for a string.Template substitution.

    >>> escape_dollar_signs('The total of my ${thing} was $5.')
    'The total of my ${thing} was $$5.'
    """
    pattern = re.compile(r'(\$)(?!{)')
    return pattern.sub(r'\1$', content)


def indent_body(content):
    lines = []

    for line in content.splitlines():
        if not line.startswith('${'):
            line = '    ' + line
        lines.append(line)

    return '\n'.join(lines)
