import unittest

from blog.text import (
    plural,
    lines,
    extract_frontmatter,
    extract_yaml,
)


class TextTestCase(unittest.TestCase):
    def test_plural(self):
        actual = plural(1, 'dude')
        expected = '1 dude'
        self.assertEqual(actual, expected, 'should return singular label')

        actual = plural(3, 'dude')
        expected = '3 dudes'
        self.assertEqual(actual, expected, 'should return plural label')

        actual = plural(3, 'box', 'boxen')
        expected = '3 boxen'
        self.assertEqual(actual, expected, 'support custom plurals')

    def test_lines(self):
        example = '''
One short sleep past, we wake eternally,
And death shall be no more; Death, thou shalt die.
'''
        expected = [
            'One short sleep past, we wake eternally,',
            'And death shall be no more; Death, thou shalt die.'
        ]

        self.assertEqual(lines(example), expected, 'should split text into lines')
        
        self.assertEqual(lines(''), [], 'should return an empty array for an empty string')

    def test_extract_frontmatter(self):
        example = '''
---
permalink: /hello/
email: dude@somebusiness.com
---
<h1>Hello!</h1>'''.lstrip()

        frontmatter, content = extract_frontmatter(example)

        expected_frontmatter = {
            'permalink': '/hello/',
            'email': 'dude@somebusiness.com'
        }

        self.assertEqual(content, '<h1>Hello!</h1>', 'should cleanly extract content')

        self.assertDictEqual(frontmatter, expected_frontmatter, 'should parse frontmatter')

    def test_extract_yaml(self):
        example = '''
a: Apple
b: Bear
c: Catastrophe
        '''

        expected = {
            'a': 'Apple',
            'b': 'Bear',
            'c': 'Catastrophe',
        }

        self.assertDictEqual(extract_yaml(example), expected)
