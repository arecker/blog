import contextlib


class StringWriter:
    """The StringWriter can be used to build documents.

    When you are done building the document, get the full string from '.text'

    >>> content = StringWriter()
    >>> content.write('line 1').write('line 2').text.splitlines()
    ['line 1', 'line 2']
    """
    def __init__(self, each_indent=2, starting_indent=0):
        self.each_indent = int(each_indent)
        self.current_indent = starting_indent
        self.text = ''

    def indent(self):
        """Increment the current indent

        >>> StringWriter().indent().current_indent
        2
        """
        self.current_indent += self.each_indent
        return self

    def unindent(self):
        """Decrement the current indent.

        >>> StringWriter().indent().unindent().current_indent
        0

        Will raise a ValueError if you try to indent too much.

        >>> StringWriter().unindent()
        Traceback (most recent call last):
        ...
        ValueError: indented too far!
        """
        result = self.current_indent - self.each_indent
        if result < 0:
            raise ValueError('indented too far!')
        self.current_indent = result
        return self

    def write(self,
              text,
              indent=False,
              unindent=False,
              blank=False,
              newline=True):
        """Write a line.

        >>> StringWriter().write('first').write('second').text.splitlines()
        ['first', 'second']

        Use indent to call indent after writing.

        >>> writer = StringWriter()
        >>> writer = writer.write('first', indent=True)
        >>> writer = writer.write('second')
        >>> writer.text.splitlines()
        ['first', '  second']
        """
        padding = self.current_indent * ' '
        self.text += f'{padding}{text}'
        if newline:
            self.text += '\n'

        if blank:
            with self.indentation_reset():
                self.write('')

        if indent:
            self.indent()
        if unindent:
            self.unindent()

        return self

    def blank(self):
        with self.indentation_reset():
            self.write('')

    def hr(self, blank=True):
        self.write('<hr/>', blank=blank)

    def br(self, blank=False):
        self.write('<br/>', blank=blank)
        
    @contextlib.contextmanager
    def indentation_reset(self):
        current = self.current_indent
        self.current_indent = 0
        yield
        self.current_indent = current

    def comment(self, text):
        self.write(f'<!-- {text} -->')

    def dl(self, data, blank=True):
        with self.block('dl', blank=blank):
            for k, v in data.items():
                self.write(f'<dt>{k}</dt>')
                self.write(f'<dd>{v}</dd>')

    def p(self, content, blank=True):
        self.write(f'<p>{content}</p>', blank=blank)
        
    def small(self, content, blank=False):
        self.write(f'<small>{content}</small>', blank=blank)

    @contextlib.contextmanager
    def block(self,
              element_name,
              blank=False,
              blank_before=False,
              _id='',
              _class='',
              _type='',
              **attributes):
        """Context manager that wraps contents in an element.

        Will reset the indentation back to its starting position, so
        do whatever you want while inside.
        """
        starting_indent = self.current_indent

        if _class:
            attributes['class'] = _class
        if _type:
            attributes['type'] = _type
        if _id:
            attributes['id'] = _id

        attributes = sorted([f'{k}="{v}"' for k, v in attributes.items()])
        attributes = ' '.join(attributes)
        attributes = attributes.strip()

        if attributes:
            self.write(f'<{element_name} {attributes}>',
                       indent=True,
                       blank=blank_before)
        else:
            self.write(f'<{element_name}>', indent=True, blank=blank_before)
        yield
        self.current_indent = starting_indent
        self.write(f'</{element_name}>', blank=blank)

    @contextlib.contextmanager
    def row(self):
        with self.block('div', _class='row', blank=True):
            yield

    @contextlib.contextmanager
    def column(self):
        with self.block('div', _class='column', blank=True):
            yield

    def figure(self, src, href='', caption='', alt='', blank=True, **attrs):
        with self.block('figure', blank=blank):
            with self.block('a', href=href or src):
                if alt:
                    self.write(f'<img src="{src}" alt="{alt}"/>')
                else:
                    self.write(f'<img src="{src}"/>')

            if caption:
                with self.block('figcaption'):
                    self.write(f'<p>{caption}</p>')

    def meta(self, name='', _property='', content='', blank=False):
        tag = '<meta'
        
        if name:
            tag += f' name="{name}"'
        if _property:
            tag += f' property="{_property}"'
        if content:
            tag += f' content="{content}"'
            
        tag += '/>'
        self.write(tag, blank=blank)
