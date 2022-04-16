import contextlib
import html


class Renderer:
    def __init__(self, starting_indent_level=0):
        self.text = ''
        self.current_indent_level = starting_indent_level

    def write(self, content: str, add_newline=True, add_blankline=False):

        indent = ' ' * self.current_indent_level
        self.text += indent + content

        if add_newline:
            self.text += '\n'

        if add_blankline:
            self.write('')

    @contextlib.contextmanager
    def indent(self, level: int):
        current = self.current_indent_level
        self.current_indent_level = level
        try:
            yield
        finally:
            self.current_indent_level = current


class MarkupRenderer(Renderer):
    each_indent = 2

    def block(self, tag_name: str, contents: str):
        tag_open = f'<{tag_name}>'
        tag_close = f'</{tag_name}>'
        contents = html.escape(contents)
        self.write(f'{tag_open}{contents}{tag_close}')

    @contextlib.contextmanager
    def wrapping_block(self, tag_name: str):
        tag_open = f'<{tag_name}>'
        tag_close = f'</{tag_name}>'

        self.write(tag_open)
        with self.indent(self.current_indent_level + self.each_indent):
            yield
        self.write(tag_close)

    def comment(self, content: str):
        content = html.escape(content)
        self.write(f'<!-- {content} -->')

    def header(self, title: str, description: str):
        with self.wrapping_block('header'):
            self.block('h1', title)
            self.block('p', description)
