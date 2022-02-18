import unittest

from .. import utils


class TestStringWriter(unittest.TestCase):
    def test_wrapper(self):
        w = utils.StringWriter()
        with w.block('test', c='2', a='1', _class='center'):
            w.write('testing')

        expected = '''
<test a="1" c="2" class="center">
  testing
</test>
'''.lstrip()

        self.assertEqual(w.text, expected)
