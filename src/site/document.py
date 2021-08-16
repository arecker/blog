import datetime
import functools
import logging
import os
import pathlib
import re

from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)


class Document:
    def __init__(self, site, page):
        self.site = site
        self.page = page

    def __repr__(self):
        return f'<Document {self.page.target}>'

    def render(self) -> str:
        html = ET.Element('html', lang='en')
        html.append(self.head())
        html.append(self.body())
        ET.indent(html)

        xml = ET.tostring(html, encoding='unicode', method='html')
        return f'<!doctype html>\n{xml}'

    @property
    def banner_url(self):
        if self.page.banner:
            return f'images/banners/{self.page.banner}'

        return None

    @property
    def meta_twitter_attrs(self):
        tags = {
            'twitter:title': self.page.title,
            'twitter:description': self.page.description,
        }

        if self.banner_url:
            tags['image'] = self.site.href(self.banner_url)

        return tags

    @property
    def meta_og_attrs(self):
        tags = {
            'url': f'/{self.page.filename}',
            'type': 'article',
            'title': self.page.title,
            'description': self.page.description,
        }

        if self.banner_url:
            tags['image'] = self.site.href(self.banner_url)

        return tags

    def head(self) -> ET.Element:
        head = ET.Element('head')

        title = ET.Element('title')
        title.text = self.page.title
        head.append(title)

        head.append(
            ET.Element('link',
                       rel='shortcut icon',
                       type='image/x-icon',
                       href='/favicon.ico'))
        head.append(
            ET.Element('link', href='/assets/site.css', rel='stylesheet'))

        head.append(ET.Element('meta', charset='UTF-8'))
        head.append(
            ET.Element('meta',
                       name='viewport',
                       content='width=device-width, initial-scale=1'))

        for k, v in self.meta_twitter_attrs.items():
            attributes = {'name': k, 'content': v}
            head.append(ET.Element('meta', **attributes))

        for k, v in self.meta_og_attrs.items():
            attributes = {'property': f'og:{k}', 'content': v}
            head.append(ET.Element('meta', **attributes))

        return head

    def body(self) -> ET.Element:
        body = ET.Element('body')
        body.append(self.header())
        body.append(ET.Element('hr'))
        body.append(self.nav())
        body.append(ET.Element('hr'))
        if self.page.banner:
            body.append(self.banner())
        body.append(self.article())
        if self.page.is_entry:
            body.append(self.pagination())
        body.append(ET.Element('hr'))
        body.append(self.footer())
        return body

    def header(self):
        tree = ET.TreeBuilder()
        tree.start('header', {})
        tree.start('h1', {})
        tree.data(self.page.title)
        tree.end('h1')
        tree.start('h2', {})
        tree.data(self.page.description)
        tree.end('h2')
        tree.end('header')
        return tree.close()

    def nav(self):
        nav = ET.Element('nav')

        for element in self.nav_breadcrumbs():
            nav.append(element)

        nav.append(self.nav_pages())

        return nav

    def nav_breadcrumbs(self):
        elements = []

        # home link
        home = ET.Element('a', href='/')
        home.text = 'index.html'
        elements.append(home)

        if self.page.filename == 'index.html':
            return elements

        divider = ET.Element('span')
        divider.text = '/'
        elements.append(divider)

        label = ET.Element('span')
        label.text = self.page.filename
        elements.append(label)

        return elements

    def nav_pages(self):
        tree = ET.TreeBuilder()

        # TODO: another class to get rid of
        tree.start('span', {'class': 'float-right-on-desktop'})

        for page in self.site.nav:
            tree.start('a', {'href': f'/{page}'})
            tree.data(page)
            tree.end('a')

        tree.end('span')
        return tree.close()

    def banner(self):
        tree = ET.TreeBuilder()
        tree.start('figure', {})
        tree.start('a', {'href': self.banner_url})
        tree.start('img', {'alt': 'banner', 'src': self.banner_url})
        tree.end('img')
        tree.end('a')
        tree.end('figure')
        return tree.close()

    def article(self):
        content = f'<article>{self.page.raw_content}</article>'
        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        parser.feed(content)
        root = parser.close()

        parent_map = {c: p for p in root.iter() for c in p}
        new_elements_map = {}

        for element in root.iter():
            if 'function Comment' not in str(element.tag):
                continue

            if not element.text.strip().startswith('blog:'):
                continue

            parent = parent_map[element]
            new_elements = self.expand_magic_comment(comment=element)
            new_elements_map[parent] = new_elements

        for parent, elements in new_elements_map.items():
            for element in elements:
                parent.append(element)

        return root

    def expand_magic_comment(self, comment):
        _, key = [t.strip() for t in comment.text.split(':')]
        comment.text = f' begin blog:{key} '
        end_comment = ET.Comment(text=f'end blog:{key}')

        if key == 'latest':
            new_elements = self.latest()
        elif key == 'entries':
            new_elements = [self.entries()]
        else:
            raise ValueError(
                f'don\'t know what to do with magic comment "{key}"')

        return new_elements + [end_comment]

    def latest(self):
        elements = []

        href = f'/{self.site.latest.filename}'
        banner_href = f'/images/banners/{self.site.latest.banner}'

        link = ET.Element('a', href=href)
        title = ET.Element('h3', attrib={'class': 'title'})
        title.text = self.site.latest.title
        link.append(title)
        elements.append(link)

        if self.site.latest.banner:
            figure = ET.Element('figure')
            link = ET.Element('a', href=href)
            image = ET.Element('img', src=banner_href)
            link.append(image)
            figure.append(link)
            caption = ET.Element('figcaption')
            caption_text = ET.Element('p')
            caption_text.text = self.site.latest.description
            caption.append(caption_text)
            figure.append(caption)
            elements.append(figure)
        else:
            caption = ET.Element('p')
            caption.text = self.site.latest.description
            elements.append(caption)

        return elements

    def entries(self):
        table = ET.Element('table')

        for entry in self.site.entries:
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

    def pagination(self):
        pages = self.site.pagination[self.page.filename]

        tree = ET.TreeBuilder()
        tree.start('nav', {'class': 'clearfix'})

        if pages.next:
            tree.start('a', {'class': 'float-left', 'href': f'/{pages.next}'})
            tree.data(f'⟵ {pages.next}')
            tree.end('a')

        if pages.previous:
            tree.start('a', {
                'class': 'float-right',
                'href': f'/{pages.previous}'
            })
            tree.data(f'{pages.previous} ⟶')
            tree.end('a')

        tree.end('nav')
        return tree.close()

    def footer(self):
        tree = ET.TreeBuilder()
        tree.start('footer', {})
        self.last_updated(tree)
        self.last_change(tree)
        self.copyright(tree)
        tree.end('footer')
        return tree.close()

    def last_updated(self, tree):
        tree.start('small', {})
        updated = self.site.timestamp.strftime("%A %B %d %Y, %I:%M %p")
        tree.data(f'Last Updated: {updated}')
        tree.end('small')

    def last_change(self, tree):
        tree.start('small', {})
        tree.data('Last Change: ')
        tree.start('span', {})
        tree.data(f'{self.site.commit.summary} (')
        tree.start('a', {'href': self.site.commit_url})
        tree.data(self.site.commit.short_hash)
        tree.end('a')
        tree.data(')')
        tree.end('span')
        tree.end('small')

    def copyright(self, tree):
        tree.start('small', {})
        year = self.site.timestamp.year
        tree.data(f'© Copyright {year} {self.site.author}')
        tree.end('small')
