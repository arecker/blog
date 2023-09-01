import argparse
import datetime
import unittest
import unittest.mock

from ..site import Site, load_site


class SiteTestCase(unittest.TestCase):
    def test_load_site(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--site-title')
        parser.add_argument('--site-description')
        parser.add_argument('--site-author')
        parser.add_argument('--site-email')

        args = parser.parse_args(
            [
                '--site-title', 'Hello',
                '--site-description', 'a website',
                '--site-author', 'Alex Recker',
                '--site-email', 'email@test.com'
            ]
        )
        site = load_site(args)
        self.assertEqual(site.title, 'Hello')
        self.assertEqual(site.description, 'a website')
        self.assertEqual(site.author, 'Alex Recker')
        self.assertEqual(site.email, 'email@test.com')

    def test_python_version(self):
        patch = unittest.mock.patch(
            'platform.python_version', return_value='1.2.3')

        with patch:
            actual = Site().python_version
            expected = 'v1.2.3'
            self.assertEqual(actual, expected)

    def test_python_executable(self):
        mock = unittest.mock.PropertyMock(return_value='/bin/fart')
        patch = unittest.mock.patch('sys.executable', new_callable=mock)

        with patch:
            actual = Site().python_executable
            expected = '/bin/fart'
            self.assertEqual(actual, expected)

    def test_url(self):
        actual = Site(protocol='http', domain='localhost').url
        expected = 'http://localhost'
        self.assertEqual(actual, expected)

    def test_timestamp(self):
        site = Site()
        expected = datetime.datetime.now()
        site._timestamp = expected
        self.assertEqual(site.timestamp, expected)
