import string

from newsrc.files import join

page_template_path = join('newsrc/templates/page.html.tmpl')


def render_page(content='', **kwargs):
    with open(page_template_path) as f:
        base_template_content = f.read()

    full_template_content = base_template_content.replace(
        '<!-- CHILD_CONTENT -->', content.replace('$', '$$'))
    full_template = string.Template(full_template_content)

    return full_template.substitute(**kwargs)
