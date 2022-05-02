import datetime
import pathlib
import tempfile
import unittest
import unittest.mock

from .. import feed


class TestFeed(unittest.TestCase):
    maxDiff = None

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
