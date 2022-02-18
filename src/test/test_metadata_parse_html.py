import unittest

from .. import utils


class TestMetadataParseHTML(unittest.TestCase):
    def test_one(self):
        actual = utils.metadata_parse_html('''
<!-- meta:title party, dumplings, and blogging -->
''')
        expected = {'title': 'party, dumplings, and blogging'}
        self.assertDictEqual(actual, expected)

    def test_two(self):
        actual = utils.metadata_parse_html('''
<!-- just a regular comment! -->
<!-- meta:title rodney stories, karta's enclosure, and ollie's championship -->
<!-- meta:banner 2022-02-14.jpg -->

<h2>Hello there!</h2>
''')
        expected = {
            'title':
            'rodney stories, karta\'s enclosure, and ollie\'s championship',
            'banner': '2022-02-14.jpg'
        }
        self.assertDictEqual(actual, expected)
