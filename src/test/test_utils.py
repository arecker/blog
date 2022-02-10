import unittest

from .. import utils


class TestStringWriter(unittest.TestCase):
    def test_wrapper(self):
        w = utils.StringWriter()
        with w.wrapper('test', a='1', c='2'):
            w.write('testing')

        expected = '''
<test a="1" c="2">
  testing
</test>
'''.lstrip()

        self.assertEqual(w.text, expected)
