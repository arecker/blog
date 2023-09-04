import unittest

from .. import xml


class TestCase(unittest.TestCase):
    def test_prettify_xml(self):
        actual = xml.prettify('<some><xml></xml></some>')
        expected = '''
<some>
  <xml />
</some>
        '''.strip()
        self.assertEqual(actual, expected)
        actual = xml.prettify('''
<!doctype html>
<h1>Hello</h1>
        '''.strip())
        expected = '''
<!doctype html>
<h1>Hello</h1>
        '''.strip()
        self.assertEqual(actual, expected)
