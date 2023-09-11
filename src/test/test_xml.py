# flake8: noqa

import unittest

from src import xml


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

        original = '''
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
  <title>Hey Reader!</title>
  <subtitle>personal online journal of Alex Recker</subtitle>
  <author>
    <name>Alex Recker</name>
    <email>alex@reckerfamily.com</email>
  </author>
  <updated>2023-09-05T00:00:00+00:00</updated>
  <id>https://www.alexrecker.com/feed.xml</id>
  <link href="https://www.alexrecker.com/feed.xml" rel="self" type="application/atom+xml" />
  <link href="https://www.alexrecker.com" rel="alternate" type="text/html" />
  <entry>
    <title>Tuesday, September 5 2023</title>
    <published>2023-09-05T00:00:00+00:00</published>
    <updated>2023-09-05T00:00:00+00:00</updated>
    <author>
      <name>Alex Recker</name>
      <email>alex@reckerfamily.com</email>
    </author>
    <id>https://www.alexrecker.com/2023-09-05.html</id>
    <link href="https://www.alexrecker.com/2023-09-05.html" />
    <media:thumbnail url="https://www.alexrecker.com/images/banners/2023-09-05.jpg" />
    <media:content medium="image" url="https://www.alexrecker.com/images/banners/2023-09-05.jpg" />
  </entry>
</feed>'''.strip()
        actual = xml.prettify(original)
        self.assertEqual(actual, original)
