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
        r.write('First', add_blankline=True)
        r.write('Second')
        self.assertEqual(r.text, 'First\n\nSecond\n')

        r.text = ''
        r.write('First', indent_level=2)
        r.write('Second', indent_level=4)
        r.write('Third')
        self.assertEqual(r.text, '  First\n    Second\nThird\n')
