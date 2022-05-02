import datetime
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
