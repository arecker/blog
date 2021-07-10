import unittest

from newsrc import partials


class PartialsTestCase(unittest.TestCase):
    def test_header(self):
        actual = partials.header(title='Title', description='Description')
        expected = '''
    <!-- partial: header -->
    <header>
      <h1 class="title">Title</h1>
      <h2 class="subtitle">Description</h2>
    </header>
    <!-- end: header -->
'''

        self.assertEqual(actual.strip(), expected.strip())
