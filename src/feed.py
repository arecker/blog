import pathlib
import xml.etree.ElementTree


def render(title='', subtitle='', author_name='', author_email='', entries=[]) -> str:
    """Render Atom rss feed."""

    tree = xml.etree.ElementTree.TreeBuilder()
    tree.start('feed', {'xmlns': 'http://www.w3.org/2005/Atom'})

    # feed title
    tree.start('title', {})
    tree.data(title)
    tree.end('title')

    # feed subtitle
    tree.start('subtitle', {})
    tree.data(subtitle)
    tree.end('subtitle')

    # feed author
    tree.start('author', {})
    tree.start('name', {})
    tree.data(author_name)
    tree.end('name')
    tree.start('email', {})
    tree.data(author_email)
    tree.end('email')
    tree.end('author')

    # last updated (use latest entry)
    tree.start('updated', {})
    tree.data(str(entries[0].date.isoformat()))
    tree.end('updated')

    # end feed
    tree.end('feed')

    document = tree.close()
    # TODO: upgrade to python 3.9 for this function
    # xml.etree.ElementTree.indent(document)

    return xml.etree.ElementTree.tostring(
        document,
        encoding='utf8',
        method='xml'
    ).decode('utf-8')


def write(www_dir='', title='', subtitle='', author_name='', author_email='', entries=[]):
    target = pathlib.Path(www_dir) / 'feed2.xml'
    with target.open('w') as f:
        f.write(render(
            title=title,
            subtitle=subtitle,
            author_name=author_name,
            author_email=author_email,
            entries=entries,
        ))
