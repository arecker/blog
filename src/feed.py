import pathlib
import urllib.parse
import xml.etree.ElementTree


def render(title='', subtitle='', author_name='', author_email='', url='', entries=[]) -> str:
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

    # link
    site_url, feed_url = urllib.parse.urlparse(url).geturl(), urllib.parse.urljoin(url, '/feed.xml')
    tree.start('id', {})
    tree.data(feed_url)
    tree.end('id')
    tree.start('link', {'rel': 'self', 'type': 'application/atom+xml', 'href': feed_url})
    tree.end('link')
    tree.start('link', {'rel': 'alternate', 'type': 'text/html', 'href': site_url})
    tree.end('link')

    # end feed
    tree.end('feed')

    document = tree.close()
    # TODO: upgrade to python 3.9 for this function
    # xml.etree.ElementTree.indent(document)

    document = xml.etree.ElementTree.tostring(
        document,
        encoding='utf-8',
        method='xml'
    ).decode('utf-8')

    return f'<?xml version="1.0" encoding="utf-8"?>{document}'


def write(www_dir='', title='', subtitle='', author_name='', author_email='', url='', entries=[]):
    target = pathlib.Path(www_dir) / 'feed2.xml'
    with target.open('w') as f:
        f.write(render(
            title=title,
            subtitle=subtitle,
            author_name=author_name,
            author_email=author_email,
            url=url,
            entries=entries,
        ))
