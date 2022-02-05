"""Functions for building and maniupulating HTML elements."""

from xml.etree import ElementTree as ET


def root():
    return ET.Element('html', lang='en')


def divider():
    return ET.Element('hr')


def row():
    return ET.Element('div', attrib={'class': 'row'})


def column():
    return ET.Element('div', attrib={'class': 'column'})


def div():
    return ET.Element('div')


def small(text='',  _class='', children=[]):
    attrib = {}

    if _class:
        attrib['class'] = _class

    el = ET.Element('small', attrib=attrib)

    if text:
        el.text = text

    for child in flatten_element_list(children, parent=el):
        el.append(child)

    return el


def br():
    return ET.Element('br')


def p(text='', children=[]):
    el = ET.Element('p')
    if text:
        el.text = text
    for child in children:
        el.append(child)
    return el


def h1(text=''):
    el = ET.Element('h1')
    el.text = text
    return el


def body():
    return ET.Element('body')


def h2(text=''):
    el = ET.Element('h2')
    if text:
        el.text = text
    return el


def h3(text='', _class=''):
    attrs = {}
    if _class:
        attrs['class'] = _class
    el = ET.Element('h3', attrib=attrs)
    if text:
        el.text = text
    return el


def link(href='', text='', children=[]):
    """Create a <a> element.

    >>> stringify_xml(link(href='google.com', text='the google'))
    '<a href="google.com">the google</a>'

    Supports child elements as well!

    >>> second = h1(text='second')
    >>> second.tail = ' some floating text'
    >>> children = [h1(text='first'), second]
    >>> stringify_xml(link(href='#', children=children), prettify=False)
    '<a href="#"><h1>first</h1><h1>second</h1> some floating text</a>'
    """
    el = ET.Element('a', attrib={'href': href})

    if text:
        el.text = text

    for child in children:
        el.append(child)

    return el


def flatten_element_list(things=[], parent=None):
    """Turns a list of elements and strings into a list of elements.

    >>> root = div()
    >>> things = [h1(text='test'), ' test ', divider()]
    >>> things = flatten_element_list(things=things)
    >>> for thing in things:
    ...     root.append(thing)
    >>> print(stringify_xml(root))
    <div>
      <h1>test</h1> test <hr>
    </div>

    Also works if the first child is a string, but if this is the case
    you should also pass in the parent element.

    >>> parent = div()
    >>> things = ['a', br()]
    >>> things = flatten_element_list(things=things, parent=parent)
    >>> for thing in things:
    ...     parent.append(thing)
    >>> print(stringify_xml(parent))
    <div>a<br>
    </div>

    Another example.

    >>> parent = div()
    >>> things = [link(href='google.com'), 'b']
    >>> things = flatten_element_list(things=things, parent=parent)
    >>> for thing in things:
    ...     parent.append(thing)
    >>> print(stringify_xml(parent))
    <div>
      <a href="google.com"></a>b</div>
    """
    new_things = []
    last_element = None

    while things:
        this_thing = things.pop(0)
        if isinstance(this_thing, ET.Element):
            new_things.append(this_thing)
            last_element = this_thing
        elif isinstance(this_thing, str):
            if last_element is not None:
                # Attach it to the tail of the last element.
                if last_element.tail:
                    last_element.tail += this_thing
                else:
                    last_element.tail = this_thing
            else:
                # Attach it to the text of the parent element.
                if parent.text:
                    parent.text += this_thing
                else:
                    parent.text = this_thing

    return new_things


def img(src=''):
    return ET.Element('img', attrib={'src': src})


def figure(src='', href='', caption=''):
    el = ET.Element('figure')
    if href:
        el.append(link(href=href, children=[img(src=src)]))
    else:
        el.append(img(src=src))

    if caption:
        figcaption = ET.Element('figcaption')
        figcaption.append(p(text=caption))
        el.append(figcaption)

    return el


def build_page_head(page_filename='',
                    page_title='',
                    page_description='',
                    page_banner_url=''):

    head = ET.Element('head')

    title = ET.Element('title')
    title.text = page_title
    head.append(title)

    head.append(
        ET.Element('link',
                   rel='shortcut icon',
                   type='image/x-icon',
                   href='./favicon.ico'))

    head.append(ET.Element('link', href='./assets/site.css', rel='stylesheet'))

    head.append(ET.Element('meta', charset='UTF-8'))

    head.append(
        ET.Element('meta',
                   name='viewport',
                   content='width=device-width, initial-scale=1'))

    twitter_tags = {
        'twitter:title': page_title,
        'twitter:description': page_description,
    }

    if page_banner_url:
        twitter_tags['image'] = page_banner_url

    for k, v in twitter_tags.items():
        attributes = {'name': k, 'content': v}
        head.append(ET.Element('meta', **attributes))

    og_tags = {
        'url': f'/{page_filename}',
        'type': 'article',
        'title': page_title,
        'description': page_description,
    }

    if page_banner_url:
        og_tags['image'] = page_banner_url

    for k, v in og_tags.items():
        attributes = {'property': f'og:{k}', 'content': v}
        head.append(ET.Element('meta', **attributes))

    return head


def _nav():
    return ET.Element('nav')


def build_page_nav(nav_pages=[], attrs={}):
    nav = ET.TreeBuilder()
    nav.start('span', attrs)

    for page in nav_pages:
        nav.start('a', {'href': f'/{page}'})
        nav.data(page)
        nav.end('a')

    nav.end('span')

    return nav.close()


def build_site_nav(filename='', nav_pages=[]):
    nav = ET.Element('nav')

    breadcrumbs = []

    home = ET.Element('a', href='/')
    home.text = 'index.html'
    breadcrumbs.append(home)

    if filename != 'index.html':
        divider = ET.Element('span')
        divider.text = '/'
        breadcrumbs.append(divider)
        label = ET.Element('span')
        label.text = filename
        breadcrumbs.append(label)

    for element in breadcrumbs:
        nav.append(element)

    nav.append(ET.Element('br', attrib={'class': 'show-on-mobile'}))
    nav.append(
        build_page_nav(nav_pages=nav_pages,
                       attrs={'class': 'float-right-on-desktop'}))

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


def build_page_banner(banner_url):
    tree = ET.TreeBuilder()
    tree.start('figure', {})
    tree.start('a', {'href': banner_url})
    tree.start('img', {'alt': 'banner', 'src': banner_url})
    tree.end('img')
    tree.end('a')
    tree.end('figure')
    return tree.close()


def build_page_article(raw_content=''):
    content = f'<article>{raw_content}</article>'
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True), )
    try:
        parser.feed(content)
        root = parser.close()
        return root
    except ET.ParseError as e:
        raise ValueError(f'{e}\n---\n{content}\n---')


def build_page_pagination(next_page='', previous_page=''):
    tree = ET.TreeBuilder()
    tree.start('nav', {'class': 'clearfix'})

    if next_page:
        tree.start('a', {'class': 'float-left', 'href': f'./{next_page}'})
        tree.data(f'⟵ {next_page}')
        tree.end('a')

    if previous_page:
        tree.start('a', {'class': 'float-right', 'href': f'./{previous_page}'})
        tree.data(f'{previous_page} ⟶')
        tree.end('a')

    tree.end('nav')
    return tree.close()


def build_page_footer(author, year):
    tree = ET.TreeBuilder()
    tree.start('footer', {})
    tree.start('small', {})
    year = year
    tree.data(f'© Copyright {year} {author}')
    tree.end('small')
    tree.end('footer')
    return tree.close()


def stringify_xml(html_tree, prettify=True):
    if prettify:
        ET.indent(html_tree)
    return ET.tostring(html_tree, encoding='unicode', method='html')


def build_link_table(rows=[], header=[]):
    if len(set([len(r) for r in rows])) != 1:
        raise ValueError('every row should have same number of columns!')

    if header and len(header) != len(rows[0]):
        raise ValueError('header should have same number of columns as rows!')

    table = ET.TreeBuilder()
    table.start('table', {})

    if header:
        table.start('tr', {})
        for col in header:
            table.start('th', {})
            table.data(col)
            table.end('th')
        table.end('tr')

    for row in rows:
        table.start('tr', {})

        # link column
        table.start('td', {})
        href = row.pop(0)
        table.start('a', {'href': href})
        table.data(href.split('/')[-1])
        table.end('a')
        table.end('td')

        # rest of columns...
        for item in row:
            table.start('td', {})
            table.data(str(item))
            table.end('td')

        table.end('tr')

    table.end('table')
    return table.close()
