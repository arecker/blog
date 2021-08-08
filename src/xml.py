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
    title = ET.Element('title')
    title.text = f'{page.title} | {page.description}'
    head.append(title)

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

    body.append(ET.Element('hr'))

    if banner := build_html_body_banner(page=page):
        body.append(banner)

    body.append(build_html_body_content(page=page, info=info))

    if pagination := build_html_body_pagination(page=page, info=info):
        body.append(pagination)

    body.append(ET.Element('hr'))

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


def build_html_body_navigation_breadcrumbs(page=None) -> [ET.Element]:
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


def build_html_body_banner(page=None) -> ET.Element:
    if not page.banner:
        return None

    url = f'/images/banners/{page.banner}'
    tree = ET.TreeBuilder()
    tree.start('figure', {})
    tree.start('a', {'href': url})
    tree.start('img', {'alt': 'banner', 'src': url})
    tree.end('img')
    tree.end('a')
    tree.end('figure')
    return tree.close()


def build_html_body_content(page=None, info=None) -> ET.Element:
    content = f'<article>{page.content}</article>'
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    parser.feed(content)
    root = parser.close()

    parent_map = {c: p for p in root.iter() for c in p}
    new_elements_map = {}

    for element in root.iter():
        if 'function Comment' not in str(element.tag):
            continue

        parent = parent_map[element]
        new_elements = expand_magic_comment(comment=element, info=info)
        new_elements_map[parent] = new_elements

    for parent, elements in new_elements_map.items():
        for element in elements:
            parent.append(element)

    return root


def expand_magic_comment(comment: ET.Element, info=None):
    _, key = [t.strip() for t in comment.text.split(':')]
    comment.text = f' begin blog:{key} '
    end_comment = ET.Comment(text=f'end blog:{key}')
    if key == 'latest':
        new_elements = build_html_latest(info=info)
    if key == 'entries':
        new_elements = [build_entries_table(entries=info.entries)]
    return new_elements + [end_comment]


def build_html_latest(info=None):
    elements = []

    href = f'/{info.latest.filename}'
    banner_href = f'/images/banners/{info.latest.banner}'

    link = ET.Element('a', href=href)
    title = ET.Element('h3', attrib={'class': 'title'})
    title.text = info.latest.title
    link.append(title)
    elements.append(link)

    if info.latest.banner:
        figure = ET.Element('figure')
        link = ET.Element('a', href=href)
        image = ET.Element('img', src=banner_href)
        link.append(image)
        figure.append(link)
        caption = ET.Element('figcaption')
        caption_text = ET.Element('p')
        caption_text.text = info.latest.description
        caption.append(caption_text)
        figure.append(caption)
        elements.append(figure)
    else:
        caption = ET.Element('p')
        caption.text = info.latest.description
        elements.append(caption)

    return elements


def build_entries_table(entries=[]) -> ET.Element:
    table = ET.Element('table')

    for entry in reversed(entries):
        row = ET.Element('tr')

        # link
        link_cell = ET.Element('td')
        link = ET.Element('a', href=f'/{entry.filename}')
        link.text = entry.filename
        link_cell.append(link)
        row.append(link_cell)

        # description
        desc_cell = ET.Element('td')
        desc_cell.text = entry.description
        row.append(desc_cell)

        table.append(row)

    return table


def build_html_body_pagination(page=None, info=None) -> ET.Element:
    if not page.is_entry():
        return None

    next_page = info.pagination[page.filename].next
    prev_page = info.pagination[page.filename].previous

    tree = ET.TreeBuilder()
    tree.start('nav', {'class': 'clearfix'})

    if next_page:
        tree.start('a', {'class': 'float-left', 'href': f'/{next_page}'})
        tree.data(f'⟵ {next_page}')
        tree.end('a')

    if prev_page:
        tree.start('a', {'class': 'float-right', 'href': f'/{prev_page}'})
        tree.data(f'{prev_page} ⟶')
        tree.end('a')

    tree.end('nav')
    return tree.close()


def build_html_body_footer(info=None, config=None):
    author = config['site']['author']
    updated = info.timestamp.strftime('%A %B %d %Y, %I:%M %p')
    url = f'https://github.com/arecker/blog/commit/{info.git.head}'
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
    tree.data(f'{info.git.head_summary} (')
    tree.start('a', {'href': url})
    tree.data(info.git.head_short)
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
