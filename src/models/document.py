import logging

from xml.etree import ElementTree as ET

from src import html as HTML

logger = logging.getLogger(__name__)


class Document:
    def __init__(self, site, page):
        self.site = site
        self.page = page

    def __repr__(self):
        return f'<Document {self.page.target}>'

    def render(self) -> str:
        html = ET.Element('html', lang='en')

        head = HTML.build_page_head(
            page_filename=self.page.filename,
            page_title=self.page.title,
            page_description=self.page.description,
            page_banner_url=self.page.banner_absolute_url)
        html.append(head)

        html.append(self.body())
        ET.indent(html)

        xml = ET.tostring(html, encoding='unicode', method='html')
        return f'<!doctype html>\n{xml}'

    def body(self) -> ET.Element:
        body = ET.Element('body')

        header = HTML.build_page_header(title=self.page.title,
                                        description=self.page.description)
        body.append(header)

        body.append(ET.Element('hr'))

        nav = HTML.build_page_nav(filename=self.page.filename,
                                  nav_pages=self.site.nav)
        body.append(nav)

        body.append(ET.Element('hr'))

        if self.page.banner:
            banner = HTML.build_page_banner(
                f'images/banners/{self.page.banner}')
            body.append(banner)

        body.append(self.article())

        if self.page.is_entry:
            pages = self.site.pagination[self.page.filename]
            pagination = HTML.build_page_pagination(
                next_page=pages.next, previous_page=pages.previous)
            body.append(pagination)

        body.append(ET.Element('hr'))

        footer = HTML.build_page_footer(author=self.site.author,
                                        year=self.site.timestamp.year)
        body.append(footer)

        return body

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

            # TODO: moving away from this type of macro.  This is a
            # shortcut until a better archive system is built out
            if 'blog:entries' not in element.text:
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

        if key == 'entries':
            new_elements = [self.entries()]

        return new_elements + [end_comment]

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
