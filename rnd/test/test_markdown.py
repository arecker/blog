import unittest

from blog.markdown import convert_emphasis


class MarkdownTestCase(unittest.TestCase):
    def test_convert_emphasis(self):
        actual = convert_emphasis('_A Christmas Carol 2: Revenge of Scrooge_')
        expected = '<em>A Christmas Carol 2: Revenge of Scrooge</em>'
        self.assertEqual(actual, expected, 'should convert underscores to emphasis')

        actual = convert_emphasis('_one_ _two_')
        expected = '<em>one</em> <em>two</em>'
        self.assertEqual(actual, expected, 'should work multiple times')

        actual = convert_emphasis('_Let me tell you a story...\njust kidding_')
        expected = '<em>Let me tell you a story...\njust kidding</em>'
        self.assertEqual(actual, expected, 'should work over multiple lines')

        actual = convert_emphasis('I am reading the book _Pride and Prejudice_.  Heard of it?')
        expected = 'I am reading the book <em>Pride and Prejudice</em>.  Heard of it?'
        self.assertEqual(actual, expected, 'should work around punctuation')

        
