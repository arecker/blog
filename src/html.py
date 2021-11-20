"""Functions for building and maniupulating HTML elements."""

from xml.etree import ElementTree as ET


def build_nav(pages=[]):
    nav = ET.Element('nav')

    for page in pages:
        link = ET.Element('a', href=f'/{page}')
        link.text = page
        nav.append(link)

    return nav


def build_page_header(title, description):
    tree = ET.TreeBuilder()
    tree.start('header', {})
    tree.start('h1', {})
    tree.data(title)
    tree.end('h1')
    tree.start('h2', {})
    tree.data(description)
    tree.end('h2')
    tree.end('header')
    return tree.close()


def stringify_xml(html_tree, prettify=True):
    if prettify:
        ET.indent(html_tree)
    return ET.tostring(html_tree, encoding='unicode', method='html')
