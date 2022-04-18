import contextlib
import html
import urllib.parse
import xml.etree.ElementTree


class Renderer:
    def __init__(self, starting_indent_level=0, each_indent=2):
        self.text = ''
        self.current_indent_level = starting_indent_level
        self.each_indent = each_indent

    def write(self, content: str, add_newline=True):
        indent = ' ' * self.current_indent_level
        self.text += indent + content
        if add_newline:
            self.text += '\n'

    @contextlib.contextmanager
    def indent(self, level: int):
        current = self.current_indent_level
        self.current_indent_level = level
        try:
            yield
        finally:
            self.current_indent_level = current

    def block(self,
              tag_name: str,
              contents='',
              self_closing=False,
              _id=None,
              _class=None,
              **attrs):

        assert not (contents and self_closing
                    ), "Can't include contents in a self-closing tag!"

        if _id:
            attrs['id'] = _id
        if _class:
            attrs['class'] = _class

        attrs = [f'{k}="{v}"' for k, v in attrs.items()]
        attrs = ' '.join(sorted(attrs)).strip()

        tag_open = f'<{tag_name}'
        if attrs:
            tag_open += f' {attrs}'
        if self_closing:
            tag_open += ' />'
            self.write(tag_open)
            return
        else:
            tag_open += '>'

        tag_close = f'</{tag_name}>'
        contents = html.escape(contents)
        self.write(f'{tag_open}{contents}{tag_close}')

    @contextlib.contextmanager
    def wrapping_block(self, tag_name: str, _id=None, _class=None, **attrs):
        if _id:
            attrs['id'] = _id
        if _class:
            attrs['class'] = _class

        attrs = [f'{k}="{v}"' for k, v in attrs.items()]
        attrs = ' '.join(sorted(attrs)).strip()

        if attrs:
            tag_open = f'<{tag_name} {attrs}>'
        else:
            tag_open = f'<{tag_name}>'

        tag_close = f'</{tag_name}>'

        self.write(tag_open)
        with self.indent(self.current_indent_level + self.each_indent):
            yield
        self.write(tag_close)

    def comment(self, content: str):
        content = html.escape(content)
        self.write(f'<!-- {content} -->')

    def meta(self, _property=None, **attrs):
        if _property:
            attrs['property'] = _property
        self.block('meta', self_closing=True, **attrs)

    def link(self, _type=None, **attrs):
        if _type:
            attrs['type'] = _type
        self.block('link', self_closing=True, **attrs)

    def newline(self):
        with self.indent(0):
            self.write('')

    def header(self, title: str, description: str):
        with self.wrapping_block('header'):
            self.block('h1', title)
            self.block('p', description)

    def figure(self, alt='', src='', href='', caption=''):
        assert alt, "All images should have an alt attribute!"
        assert src, "All images should have an src attribute!"

        with self.wrapping_block('figure'):
            with self.wrapping_block('a', href=href or src):
                self.block('img', src=src, alt=alt, self_closing=True)
            if caption:
                with self.wrapping_block('figcaption'):
                    self.block('p', caption)

    def breadcrumbs(self, filename):
        with self.wrapping_block('nav'):
            self.block('a', href='./index.html', contents='index.html')
            if filename != 'index.html':
                self.block('span', contents=f'/ {filename}')

    def hr(self):
        self.block('hr', self_closing=True)

    def footer(self, author='', year=''):
        with self.wrapping_block('footer'):
            self.block('small', contents=f'© Copyright {year} {author}')

    def as_html(self):
        result = f'''
<!doctype html>
<html lang="en">

{self.text}
</html>
'''.lstrip()

        return result

    def as_xml(self):
        result = f'''
<?xml version="1.0" encoding="utf-8"?>
{self.text}'''.lstrip()

        xml.etree.ElementTree.fromstring(result)
        return result


def render_page(page, full_url: str):
    r = Renderer()

    with r.wrapping_block('head'):
        r.block('title', contents=page.title)
        r.newline()

        r.comment('Page Assets')
        r.link(rel='shortcut icon', _type='image/x-icon', href='./favicon.ico')
        r.link(rel='stylesheet', href='./assets/site.css')
        r.newline()

        r.comment('Page Metadata')
        r.meta(charset='UTF-8')
        r.meta(name='viewport', content='width=device-width, initial-scale=1')
        r.meta(name='twitter:title', content=page.title)
        r.meta(name='twitter:description', content=page.description)
        r.meta(name='og:url', content=urllib.parse.urljoin(full_url, page.filename))
        r.meta(_property='og:type', content='article')
        r.meta(_property='og:title', content=page.title)
        r.meta(_property='og:description', content=page.description)
        r.newline()

    return r.as_html()
