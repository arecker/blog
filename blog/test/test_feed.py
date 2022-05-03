import datetime
import pathlib
import tempfile
import unittest
import unittest.mock

from .. import feed


class TestFeed(unittest.TestCase):
    maxDiff = None

    def test_plain_textify(self):
        self.assertEqual(feed.plain_textify('Hello there'), 'Hello there')

        self.assertEqual(
            feed.plain_textify('''
<p>Some easy paragraphs.</p>

<p>Can it handle paragraphs?</p>
'''), '''
Some easy paragraphs.

Can it handle paragraphs?
''')
        self.assertEqual(
            feed.plain_textify('''
<p>Some <em>italics</em>, <strong>strongs</strong>, or <b>bolds</b> in a paragraph?</p>
'''), '''
Some italics, strongs, or bolds in a paragraph?
''')

        self.assertEqual(feed.plain_textify('<a href="google.com">a link</a>'),
                         '[a link]')

        self.assertEqual(
            feed.plain_textify('''
<!-- this is a comment -->
''').strip(), '')

        actual = feed.plain_textify('''
<figure>
  <a href="./images/2022-04-14-lunch.jpg">
    <img alt="lunch" src="./images/2022-04-14-lunch.jpg"/>
  </a>
</figure>
''')

        expected = '''
[figure lunch]
'''
        self.assertEqual(actual, expected)

        actual = feed.plain_textify('''
<figure>
  <a href="./images/2022-04-13-ziggy.jpg">
    <img alt="ziggy" src="./images/2022-04-13-ziggy.jpg"/>
  </a>
  <figcaption><p>Be strong, Ziggy.  We'll get through this.</p></figcaption>
</figure>
''')

        expected = '''
[figure ziggy: Be strong, Ziggy.  We'll get through this.]
'''
        self.assertEqual(actual, expected)

        actual = feed.plain_textify('''
<video width="400" controls="">
  <source src="/vids/2022-04-06-studio-dog.webm" type="video/webm" />
  Bummer - it looks like your browser doesn't support embedded video.
</video>
''')

        expected = '''
[video studio-dog]
'''

        self.assertEqual(actual, expected)

    def test_render_feed_info(self):
        expected = '''
<title>Dear Journal</title>
<subtitle>Daily, public journal by Alex Recker</subtitle>
<author>
  <name>Alex Recker</name>
  <email>alex@reckerfamily.com</email>
</author>
<updated>2021-01-01T00:00:00+00:00</updated>
<id>https://www.alexrecker.com/feed.xml</id>
<link href="https://www.alexrecker.com/feed.xml" rel="self" type="application/atom+xml" />
<link href="https://www.alexrecker.com" rel="alternate" type="text/html" />
'''.lstrip()

        info = feed.Info(title='Dear Journal',
                         subtitle='Daily, public journal by Alex Recker',
                         author_name='Alex Recker',
                         author_email='alex@reckerfamily.com',
                         timestamp=datetime.datetime(2021, 1, 1),
                         full_url='https://www.alexrecker.com')

        actual = feed.render_feed_info(info)

        self.assertEqual(actual, expected)

    def test_render_feed_entry(self):
        info = unittest.mock.Mock(author_name='Alex Recker',
                                  author_email='alex@reckerfamily.com',
                                  full_url='https://www.alexrecker.com')

        with tempfile.TemporaryDirectory() as d:
            source = pathlib.Path(d) / 'testing.html'

            with source.open('w') as f:
                f.write('TESTING')

            entry = unittest.mock.Mock(
                title='Just a Test Entry',
                description='a test entry for a unit test',
                date=datetime.datetime(2019, 1, 1),
                filename='testing.html',
                banner='testing.jpg',
                source=str(source))

            actual = feed.render_feed_entry(entry, info)

        expected = '''
<entry>
  <title>Just a Test Entry</title>
  <summary><![CDATA[a test entry for a unit test]]></summary>
  <published>2019-01-01T00:00:00+00:00</published>
  <updated>2019-01-01T00:00:00+00:00</updated>
  <author>
    <name>Alex Recker</name>
    <email>alex@reckerfamily.com</email>
  </author>
  <id>https://www.alexrecker.com/testing.html</id>
  <link href="https://www.alexrecker.com/testing.html" />
  <media:thumbnail url="https://www.alexrecker.com/images/banners/testing.jpg" xmlns:media="http://search.yahoo.com/mrss/" />
  <media:content medium="image" url="https://www.alexrecker.com/images/banners/testing.jpg" xmlns:media="http://search.yahoo.com/mrss/" />
  <content><![CDATA[TESTING]]></content>
</entry>
'''.lstrip()

        self.assertEqual(actual, expected)

    def test_render_feed(self):
        info = unittest.mock.Mock(
            title='Dear Journal',
            subtitle='Daily, public journal by Alex Recker',
            author_name='Alex Recker',
            author_email='alex@reckerfamily.com',
            full_url='https://www.alexrecker.com',
            timestamp=datetime.datetime(2019, 1, 1))

        with tempfile.TemporaryDirectory() as d:
            source = pathlib.Path(d) / 'testing.html'

            with source.open('w') as f:
                f.write('TESTING')

            entry = unittest.mock.Mock(
                title='Just a Test Entry',
                description='a test entry for a unit test',
                date=datetime.datetime(2019, 1, 1),
                filename='testing.html',
                banner='testing.jpg',
                source=str(source))

            actual = feed.render_feed(info, entries=[entry])

        expected = '''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Dear Journal</title>
  <subtitle>Daily, public journal by Alex Recker</subtitle>
  <author>
    <name>Alex Recker</name>
    <email>alex@reckerfamily.com</email>
  </author>
  <updated>2019-01-01T00:00:00+00:00</updated>
  <id>https://www.alexrecker.com/feed.xml</id>
  <link href="https://www.alexrecker.com/feed.xml" rel="self" type="application/atom+xml" />
  <link href="https://www.alexrecker.com" rel="alternate" type="text/html" />
  <entry>
    <title>Just a Test Entry</title>
    <summary><![CDATA[a test entry for a unit test]]></summary>
    <published>2019-01-01T00:00:00+00:00</published>
    <updated>2019-01-01T00:00:00+00:00</updated>
    <author>
      <name>Alex Recker</name>
      <email>alex@reckerfamily.com</email>
    </author>
    <id>https://www.alexrecker.com/testing.html</id>
    <link href="https://www.alexrecker.com/testing.html" />
    <media:thumbnail url="https://www.alexrecker.com/images/banners/testing.jpg" xmlns:media="http://search.yahoo.com/mrss/" />
    <media:content medium="image" url="https://www.alexrecker.com/images/banners/testing.jpg" xmlns:media="http://search.yahoo.com/mrss/" />
    <content><![CDATA[TESTING]]></content>
  </entry>
</feed>
'''

        self.assertEqual(actual, expected)

    def test_write_feed(self):
        with tempfile.TemporaryDirectory() as d:
            source = pathlib.Path(d) / 'test.html'
            with source.open('w') as f:
                f.write('TESTING')

            entry = unittest.mock.Mock(
                title='Just a Test Entry',
                description='a test entry for a unit test',
                date=datetime.datetime(2019, 1, 1),
                filename='testing.html',
                banner='testing.jpg',
                source=str(source))

            feed.write_feed(d,
                            title='Test Title',
                            subtitle='Test Subtitle',
                            author_name='Alex',
                            author_email='me@me.com',
                            timestamp=datetime.datetime(2019, 1, 1),
                            full_url='http://localhost',
                            entries=[entry])

            expected = pathlib.Path(d) / 'feed.xml'
            self.assertTrue(expected.is_file())
