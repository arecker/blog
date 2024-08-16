import xml.etree.ElementTree


xml.etree.ElementTree.register_namespace("", "http://www.w3.org/2005/Atom")
xml.etree.ElementTree.register_namespace("media", "http://search.yahoo.com/mrss/")


def prettify(content: str) -> str:
    """Prettify an XML string

    Raises a `ValueError` if the input is invalid.

    >>> prettify('<some><xml></xml></some>')
    <some>
      <xml />
    </some>
    """
    # if there is a doctype, trim it off
    doctype, *rest = content.splitlines()
    doctype = doctype.lower()
    if doctype.startswith('<!doctype') or doctype.startswith('<?xml'):
        content = '\n'.join(rest)
    else:
        doctype = None

    # escape special characters
    content = content.replace('&', '&amp;')

    # convert to a tree
    try:
        tree = xml.etree.ElementTree.fromstring(content)
    except xml.etree.ElementTree.ParseError as e:
        raise ValueError(f'error parsing the following ({e.args})\n{content[:800]}')

    # add indenting
    xml.etree.ElementTree.indent(tree)

    # decode back to string
    content = xml.etree.ElementTree.tostring(
        tree, encoding='utf8').decode('utf-8')

    # trim off the first line, which is the doctype
    content = '\n'.join(content.splitlines()[1:])

    # reattach the original doctype, if there was one.
    if doctype:
        content = doctype + '\n' + content

    return content
