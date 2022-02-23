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
        """Add a blank line.

        >>> StringWriter().blank().text.splitlines()
        ['']
        """
        with self.indentation_reset():
            self.write('')
        return self

    def hr(self, blank=True):
        """Add an <hr/> element.

        >>> StringWriter().hr().text.strip()
        '<hr/>'
        """
        return self.write('<hr/>', blank=blank)

    def br(self, blank=False):
        """Add a <br/> element.

        >>> StringWriter().br().text.strip()
        '<br/>'
        """
        return self.write('<br/>', blank=blank)

    @contextlib.contextmanager
    def indentation_reset(self):
        current = self.current_indent
        self.current_indent = 0
        yield
        self.current_indent = current

    def comment(self, text):
        """Write an HTML comment.
        
        >>> writer = StringWriter()
        >>> writer.comment('Test Comment').text.strip()
        '<!-- Test Comment -->'
        """
        return self.write(f'<!-- {text} -->')

    def dl(self, data: dict, blank=True):
        """Make a definition list.

        >>> data = {'fruit': 'bananana', 'vegetable': 'carrot'}
        >>> print(StringWriter().dl(data).text.strip())
        <dl>
          <dt>fruit</dt>
          <dd>bananana</dd>
          <dt>vegetable</dt>
          <dd>carrot</dd>
        </dl>
        """
        with self.block('dl', blank=blank):
            for k, v in data.items():
                self.write(f'<dt>{k}</dt>')
                self.write(f'<dd>{v}</dd>')
        return self

    def ul(self, items, blank=True):
        """Make an unordered list.

        >>> items = ['banana', 'orange', 'apple']
        >>> print(StringWriter().ul(items).text.strip())
        <ul>
          <li>banana</li>
          <li>orange</li>
          <li>apple</li>
        </ul>
        """
        with self.block('ul', blank=blank):
            for item in items:
                self.write(f'<li>{item}</li>')
        return self

    def pre(self, content, blank=True):
        """Write a pre element
        
        >>> print(StringWriter().pre('hostname').text.strip())
        <pre>hostname</pre>
        """
        return self.write(f'<pre>{content}</pre>', blank=True)

    def h2(self, content, blank=True):
        """Write an h2 element.

        >>> StringWriter().h2('testing').text.strip()
        '<h2>testing</h2>'
        """
        return self.write(f'<h2>{content}</h2>', blank=blank)

    def p(self, content, blank=True):
        """Write a p element.

        >>> StringWriter().p('testing').text.strip()
        '<p>testing</p>'
        """
        return self.write(f'<p>{content}</p>', blank=blank)

    def small(self, content, blank=False):
        """Return a <small> element.

        >>> StringWriter().small('testing').text.strip()
        '<small>testing</small>'
        """
        return self.write(f'<small>{content}</small>', blank=blank)

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

        >>> writer = StringWriter()
        >>> with writer.block('example'):
        ...     writer = writer.write('inside the block!')
        >>> writer.text.splitlines()
        ['<example>', '  inside the block!', '</example>']

        Supports attributes too (use underscores for reserved python
        words like "class" and "id").

        >>> writer = StringWriter()
        >>> with writer.block('div', style='color: red', _class='row'):
        ...     _ = writer.comment('Inside the row')
        >>> writer.text.splitlines()
        ['<div class="row" style="color: red">', '  <!-- Inside the row -->', '</div>']
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

    def figure(self, src, href='', caption='', alt='', blank=True, **attrs):
        """Make an HTML figure.  

        As a convenience to the viewer, by default the image thumbnail
        is wrapped in a hyperlink to the original image.
        
        >>> writer = StringWriter()
        >>> writer.figure('test.jpg', alt='a test image')
        >>> writer.text.strip().splitlines()
        ['<figure>', '  <a href="test.jpg">', '    <img src="test.jpg" alt="a test image"/>', '  </a>', '</figure>']

        Pass in a caption to the image.

        >>> writer = StringWriter()
        >>> writer.figure('test.jpg', alt='a test image', caption='this is the caption')
        >>> writer.text.strip().splitlines()
        ['<figure>', '  <a href="test.jpg">', '    <img src="test.jpg" alt="a test image"/>', '  </a>', '  <figcaption>', '    <p>this is the caption</p>', '  </figcaption>', '</figure>']
        """
        assert alt, 'Every image should have an alt!'
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
        """Add a meta property.

        >>> writer = StringWriter()
        >>> writer.meta(name='description', content='bleh')
        >>> writer.meta(_property='og:url', content='google.com')
        >>> writer.text.strip().splitlines()
        ['<meta name="description" content="bleh"/>', '<meta property="og:url" content="google.com"/>']
        """

        tag = '<meta'

        if name:
            tag += f' name="{name}"'
        if _property:
            tag += f' property="{_property}"'
        if content:
            tag += f' content="{content}"'

        tag += '/>'
        self.write(tag, blank=blank)
