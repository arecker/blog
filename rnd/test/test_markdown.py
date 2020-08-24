import os
import unittest

from blog import files
from blog.pages import Entry
from blog.markdown import (
    convert_emphasis,
    convert_bold,
    convert_links,
    convert_headings,
    convert_code,
    convert_paragraphs,
    convert,
    LinkReplacer
)


class LinkReplacerTestCase(unittest.TestCase):
    def test_strip(self):
        '''
        should remove all links from the final document
        '''
        example = '''This is a [test].

[test]: https://google.com

And one more thing.  I have something
[tricky] that I want to test.

[tricky]: askjeeves.biz'''

        actual = LinkReplacer(example).extract().strip().subject
        expected = '''This is a [test].


And one more thing.  I have something
[tricky] that I want to test.
'''
        self.assertEqual(actual, expected)

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

        actual = convert_emphasis('Email me at the_dude@the_netthe_net.org')
        expected = 'Email me at the_dude@the_netthe_net.org'
        self.assertEqual(actual, expected, 'should ignore underscores in the middle of a string')

        actual = convert_emphasis('I am reading the book _Pride and Prejudice_.  Heard of it?')
        expected = 'I am reading the book <em>Pride and Prejudice</em>.  Heard of it?'
        self.assertEqual(actual, expected, 'should work around punctuation')

    def test_convert_bold(self):
        actual = convert_bold('**Gasp**')
        expected = '<strong>Gasp</strong>'
        self.assertEqual(actual, expected, 'should convert double asterisks to emphasis')

        actual = convert_bold('**Gasp** and **shock**')
        expected = '<strong>Gasp</strong> and <strong>shock</strong>'
        self.assertEqual(actual, expected, 'should work multiple times')

    def test_convert_links(self):
        example = '''
Here is the [first thing], and the [second thing].
[first thing]: https://google.com/blah/
[second thing]: https://google.com/blerp/
'''

        expected = '''
Here is the <a href="https://google.com/blah/">first thing</a>, and the <a href="https://google.com/blerp/">second thing</a>.
'''
        self.assertEqual(convert_links(example), expected, 'should extract and convert links')

        example = r'"This is \[not\] a link," said Alex.'
        expected = r'"This is [not] a link," said Alex.'
        self.assertEqual(convert_links(example), expected, 'should escape backslashed links')

        actual = convert_links('[google](https://google.com)')
        expected = '<a href="https://google.com">google</a>'
        self.assertEqual(actual, expected, 'should convert simple inline links')

    def test_convert_headings(self):
        example = '''
# First

## Second

### Third
        '''

        actual = convert_headings(example)

        expected = '''
<h1>First</h1>

<h2>Second</h2>

<h3>Third</h3>
        '''

        self.assertEqual(actual, expected, 'should convert to appropriate heading tags')

    def test_convert_code(self):
        example = '''
```lisp
(defun hello-world()
  (if (something-p) 4 3))
```'''

        expected = '''
<pre class="lisp">
(defun hello-world()
  (if (something-p) 4 3))
</pre>'''

        self.assertEqual(convert_code(example), expected, 'should convert code blocks with language')

    def test_paragraphs(self):
        example = 'This is a test.'
        actual = convert_paragraphs(example)
        expected = '<p>This is a test.</p>'
        self.assertEqual(actual, expected, 'should handle single paragraphs')

        example = '''This is a test.

This is another paragraph.'''
        actual = convert_paragraphs(example)
        expected = '''<p>This is a test.</p>

<p>This is another paragraph.</p>'''
        self.assertEqual(actual, expected, 'should handle multiple paragraphs')

    def test_entries(self):
        for example in self.fixtures('entries'):
            basename, _ = os.path.splitext(example)
            entry = Entry(files.join(f'entries/{basename}.md'))
            actual = entry.render()
            with open(self.fixture_join('entries', example)) as f:
                expected = f.read()
            self.assertEqual(actual, expected, f'{entry.src} should match {example}')

    def fixture_join(self, subpath, fixture=None):
        _dir = files.join('rnd/test/fixtures/', subpath)
        if fixture:
            return os.path.join(_dir, fixture)
        else:
            return _dir

    def fixtures(self, subpath):
        return os.listdir(self.fixture_join(subpath))
