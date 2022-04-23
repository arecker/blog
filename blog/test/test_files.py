import contextlib
import datetime
import pathlib
import tempfile
import unittest
import unittest.mock

from .. import files


@contextlib.contextmanager
def temp_root():
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        (d / 'entries').mkdir()
        yield d


class TestFiles(unittest.TestCase):

    def test_is_not_junk_file(self):
        self.assertTrue(files.is_not_junk_file('test.html'))
        self.assertTrue(files.is_not_junk_file(pathlib.Path('test.html')))
        self.assertFalse(files.is_not_junk_file(
            pathlib.Path('.something.tmp')))
        self.assertFalse(files.is_not_junk_file(pathlib.Path('#test.html')))

    def test_paginate_files(self):
        result = files.paginate_files(['a', 'b', 'c'])
        self.assertIsNone(result['a'].previous)
        self.assertEqual(result['a'].next, 'b')
        self.assertEqual(result['c'].previous, 'b')
        self.assertIsNone(result['c'].next)

    def test_new_entry(self):
        with temp_root() as root:
            with open(root / 'entries/2021-01-01.html', 'w') as f:
                f.write(f'''
<!-- meta:title a smoothie -->
<!-- meta:banner smoothie.jpg -->

I had a really delicious smoothie from Surf City Squeeze.
'''.lstrip())

            pagination = {
                '2021-01-01.html': unittest.mock.Mock(next=None, previous=None)
            }
            entry = files.new_entry(root / 'entries/2021-01-01.html',
                                    pagination=pagination)
            self.assertEqual(entry.filename, '2021-01-01.html')
            self.assertEqual(entry.title, 'Friday, January 1 2021')
            self.assertEqual(entry.date, datetime.datetime(2021, 1, 1))
            self.assertEqual(entry.source, root / 'entries/2021-01-01.html')
            self.assertEqual(entry.banner, 'smoothie.jpg')
            self.assertEqual(entry.description, 'a smoothie')

    def test_all_entries(self):
        with temp_root() as root:
            slugs = [
                '2021-01-01',  # 0
                '2023-04-12',  # 1
                '1990-09-29'  # 2
            ]
            for i, slug in enumerate(slugs):
                with open(root / f'entries/{slug}.html', 'w') as f:
                    f.write(f'''
<!-- meta:title Test Entry {i} -->
<!-- meta:banner test.jpg -->

This is a test entry, made from a unit test from slug {slug}.
'''.lstrip())

            entries = files.all_entries(root / 'entries')

            newest = entries[0]
            self.assertEqual(newest.filename, '2023-04-12.html')
            self.assertEqual(newest.title, 'Wednesday, April 12 2023')
            self.assertEqual(newest.date, datetime.datetime(2023, 4, 12))
            self.assertEqual(newest.source, root / 'entries/2023-04-12.html')
            self.assertEqual(newest.banner, 'test.jpg')
            self.assertEqual(newest.description, 'Test Entry 1')
            self.assertEqual(newest.page_next, '2021-01-01.html')
            self.assertEqual(newest.page_previous, None)
