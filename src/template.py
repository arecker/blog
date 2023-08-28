import logging
import xml.etree.ElementTree

import jinja2


logger = logging.getLogger('blog')
template_loader = jinja2.FileSystemLoader(searchpath='./templates')
template_env = jinja2.Environment(loader=template_loader)


def prettify_xml(content: str) -> str:
    """
    Returns a prettified version of the XML document in `content` as a
    `str`.

    Warning: this raises a `xml.etree.ElementTree.ParseError` if there
    is *anything* invalid in the document, and - being XML - it's kind
    of picky.
    """
    tree = xml.etree.ElementTree.fromstring(content)
    xml.etree.ElementTree.indent(tree)
    content = xml.etree.ElementTree.tostring(
        tree, encoding='utf8', method='html').decode('utf-8')
    return content


def render_template(template_name: str, context={}):
    """
    Render a template into a string.
    """
    template = template_env.get_template(template_name)
    return template.render(**context)
