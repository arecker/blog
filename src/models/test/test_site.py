import unittest
import unittest.mock

from ..site import Site


class SiteTestCase(unittest.TestCase):
    def test_python_version(self):
        patch = unittest.mock.patch(
            'platform.python_version', return_value='1.2.3')
        with patch:
            actual = Site().python_version
            expected = 'v1.2.3'
            self.assertEqual(actual, expected)
