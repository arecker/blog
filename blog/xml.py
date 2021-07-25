from xml.etree import ElementTree as ET


def build_html_page(page=None, config=None, info=None) -> str:
    html = ET.Element('html', lang='en')

    head = build_html_head(page=page, config=config)
    html.append(head)

    body = build_html_body(page=page, config=config, info=info)
    html.append(body)

    ET.indent(html)
    xml = ET.tostring(html, encoding='unicode', method='html')
    return f'<!doctype html>\n{xml}'


def build_html_head(page=None, config=None):
    head = ET.Element('head')

    # title
    head.append(ET.Element('head', text=f'{page.title} | {page.description}'))

    # link
    head.append(
        ET.Element('link',
                   rel='shortcut icon',
                   type='image/x-icon',
                   href='/favicon.ico'))
    head.append(ET.Element('link', href='/assets/site.css', rel='stylesheet'))

    # meta
    head.append(ET.Element('meta', charset='UTF-8'))
    head.append(
        ET.Element('meta',
                   name='viewport',
                   content='width=device-width, initial-scale=1'))

    # twitter
    twitter_tags = {
        'twitter:title': page.title,
        'twitter:description': page.description,
    }

    if page.banner:
        banner_url = f'https://www.alexrecker.com/images/banners/{page.banner}'
        twitter_tags['image'] = banner_url

    for k, v in twitter_tags.items():
        attributes = {'name': k, 'content': v}
        head.append(ET.Element('meta', **attributes))

    # og
    og_tags = {
        'url': f'/{page.filename}',
        'type': 'article',
        'title': page.title,
        'description': page.description,
    }

    for k, v in og_tags.items():
        attributes = {'property': f'og:{k}', 'content': v}
        head.append(ET.Element('meta', **attributes))

    return head


def build_html_body(page=None, config=None, info=None):
    body = ET.Element('body')

    header = build_html_body_header(page=page)
    body.append(header)

    body.append(ET.Element('hr'))

    nav = build_html_body_navigation(page=page, config=config)
    body.append(nav)

    footer = build_html_body_footer(info=info, config=config)
    body.append(footer)

    return body


def build_html_body_header(page=None):
    tree = ET.TreeBuilder()
    tree.start('header', {})
    tree.start('h1', {})
    tree.data(page.title)
    tree.end('h1')
    tree.start('h2', {})
    tree.data(page.description)
    tree.end('h2')
    tree.end('header')
    return tree.close()


def build_html_body_navigation(page=None, config=None):
    nav_pages = [i.strip() for i in config['site'].get('nav', '').split(',')]

    nav = ET.Element('nav')

    for element in build_html_body_navigation_breadcrumbs(page=page):
        nav.append(element)

    # TODO: get rid of CSS class
    nav.append(ET.Element('br', attrib={'class': 'show-on-mobile'}))

    nav.append(build_html_body_navigation_pages(pages=nav_pages))

    return nav


def build_html_body_navigation_breadcrumbs(page=None):
    elements = []

    # home link
    home = ET.Element('a', href='/')
    home.text = 'index.html'
    elements.append(home)

    if page.filename == 'index.html':
        return elements

    divider = ET.Element('span')
    divider.text = '/'
    elements.append(divider)

    label = ET.Element('span')
    label.text = page.filename
    elements.append(label)

    return elements


def build_html_body_navigation_pages(pages=[]) -> ET.Element:
    tree = ET.TreeBuilder()

    # TODO: another class to get rid of
    tree.start('span', {'class': 'float-right-on-desktop'})

    for page in pages:
        tree.start('a', {'href': f'/{page}'})
        tree.data(page)
        tree.end('a')

    tree.end('span')
    return tree.close()


def build_html_body_footer(info=None, config=None):
    author = config['site']['author']
    updated = info.timestamp.strftime('%A %B %d %Y, %I:%M %p')
    url = f'https://github.com/arecker/blog/commit/{info.git_head}'
    year = info.timestamp.year

    tree = ET.TreeBuilder()
    tree.start('footer', {})

    # Last Updated
    tree.start('small', {})
    tree.data(f'Last Updated: {updated}')
    tree.end('small')

    # Last Change
    tree.start('small', {})
    tree.data('Last Change: ')
    tree.start('span', {})
    tree.data(f'{info.git_head_summary} (')
    tree.start('a', {'href': url})
    tree.data(info.git_head_short)
    tree.end('a')
    tree.data(')')
    tree.end('span')
    tree.end('small')

    # Copyright
    tree.start('small', {})
    tree.data(f'© Copyright {year} {author}')
    tree.end('small')

    tree.end('footer')
    return tree.close()
