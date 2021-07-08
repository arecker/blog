import string

from .files import join
from .logger import logger as l


page_template_path = join('newsrc/templates/page.html.tmpl')
with open(page_template_path) as f:
    page_template = string.Template(f.read())
    l.debug('loaded page template from %s', page_template_path)


def render_page(**kwargs):
    return page_template.substitute(**kwargs)
