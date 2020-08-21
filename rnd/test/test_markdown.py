import unittest

from blog.markdown import (
    convert_emphasis,
    convert_bold,
    convert_links,
    convert_headings,
    convert_code,
    convert
)


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

    def test_convert(self):

        # ALL TOGETHER NOW

        example = '''
# Introduction (the _real_ intro)

Here is an [inline link](alexrecker.com).

Taken from the book **_Moby Dick_**:
"Call me _**Ishmael**_."

**HIT ME UP ON [MAH TWITTAH]!!!**

How about some code?

```ruby
puts "ruby sucks"
```

[MAH TWITTAH]: https://www.twitter.com/@alex_recker'''.strip()

        expected = '''
<h1>Introduction (the <em>real</em> intro)</h1>

Here is an <a href="alexrecker.com">inline link</a>.

Taken from the book <strong><em>Moby Dick</em></strong>:
"Call me <em><strong>Ishmael</strong></em>."

<strong>HIT ME UP ON <a href="https://www.twitter.com/@alex_recker">MAH TWITTAH</a>!!!</strong>

How about some code?

<pre class="ruby">
puts "ruby sucks"
</pre>
'''.strip()

        self.assertEqual(convert(example).strip(), expected, 'should correctly convert markdown')
