import datetime
import unittest

from .. import dump_json
from .. import load_json


class TestJson(unittest.TestCase):
    def test_load_json(self):
        content = '''
{"filename": "2019-07-02.html", "title": "Tuesday, July 2 2019", "description": "party, dumplings, and blogging", "banner": null, "date": "2019-07-02T00:00:00"}'''.strip()

        actual = load_json(content)
        self.assertIsInstance(actual['date'], datetime.datetime)
        self.assertIsNone(actual['banner'])

    def test_dump_json(self):
        page = {
            'date': datetime.datetime(1990, 9, 29),
            'banner': None,
        }

        actual = dump_json(page)
        expected = '''
{"banner": null, "date": "1990-09-29T00:00:00"}
        '''.strip()
        self.assertEqual(actual, expected)
