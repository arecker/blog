"""Functions for building and maniupulating HTML elements."""

from xml.etree import ElementTree as ET


def root():
    return ET.Element('html', lang='en')


def divider():
    return ET.Element('hr')


def div():
    return ET.Element('div')


def p():
    return ET.Element('p')


def body():
    return ET.Element('body')


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
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    parser.feed(content)
    root = parser.close()
    return root


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
