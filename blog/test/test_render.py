import unittest

from ..render import Renderer


class TestRenderer(unittest.TestCase):
    def test_write(self):
        r = Renderer()
        self.assertEqual(r.text, '')

        r.write('First line')
        self.assertEqual(r.text, 'First line\n')

        r.write('Second line')
        self.assertEqual(r.text, 'First line\nSecond line\n')

        r.text = ''
        r.write('no newline!', add_newline=False)
        self.assertEqual(r.text, 'no newline!')

        r.text = ''
        r.current_indent_level = 2
        r.write('First')

        r.current_indent_level = 4
        r.write('Second')

        r.current_indent_level = 0
        r.write('Third')
        self.assertEqual(r.text, '  First\n    Second\nThird\n')

    def test_indent(self):
        r = Renderer()

        r.write('Unindented.')

        with r.indent(2):
            r.write('Indented!')

        r.write('Unindented.')

        self.assertEqual(r.text, 'Unindented.\n  Indented!\nUnindented.\n')

    def test_block(self):
        r = Renderer()
        r.block('p', contents='This is a paragraph.')
        self.assertEqual(r.text.strip(), '<p>This is a paragraph.</p>')

        r = Renderer()
        r.block('p', 'Unsafe characters, like "&", "<", and ">"')
        self.assertEqual(
            r.text.strip(), '<p>Unsafe characters, like '
            '&quot;&amp;&quot;, '
            '&quot;&lt;&quot;, and '
            '&quot;&gt;&quot;</p>')

    def test_wrapping_block(self):
        r = Renderer()
        with r.wrapping_block('a'):
            r.block('b', 'nested!')
        self.assertEqual(r.text, '''
<a>
  <b>nested!</b>
</a>
'''.lstrip())

    def test_comment(self):
        r = Renderer()
        r.comment('A comment')
        self.assertEqual(r.text, '<!-- A comment -->\n')

    def test_newline(self):
        r = Renderer()
        r.write('hello')
        r.newline()
        r.write('hello again')
        self.assertEqual(r.text, 'hello\n\nhello again\n')

    def test_header(self):
        r = Renderer(starting_indent_level=4)
        r.header('Test page', 'Just a test page!')
        self.assertEqual(
            r.text, '''    <header>
      <h1>Test page</h1>
      <p>Just a test page!</p>
    </header>
''')
