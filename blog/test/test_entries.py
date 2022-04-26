import contextlib
import datetime
import pathlib
import tempfile
import unittest
import unittest.mock

from .. import entries


@contextlib.contextmanager
def temp_root():
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        (d / 'entries').mkdir()
        (d / 'www').mkdir()
        yield d


class TestEntries(unittest.TestCase):

    def test_is_not_junk_file(self):
        self.assertTrue(entries.is_not_junk_file('test.html'))
        self.assertTrue(entries.is_not_junk_file(pathlib.Path('test.html')))
        self.assertFalse(
            entries.is_not_junk_file(pathlib.Path('.something.tmp')))
        self.assertFalse(entries.is_not_junk_file(pathlib.Path('#test.html')))

    def test_paginate_files(self):
        result = entries.paginate_files(['a', 'b', 'c'])
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
            entry = entries.new_entry(root / 'entries/2021-01-01.html',
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

            _entries = entries.all_entries(root / 'entries')

            newest = _entries[0]
            self.assertEqual(newest.filename, '2023-04-12.html')
            self.assertEqual(newest.title, 'Wednesday, April 12 2023')
            self.assertEqual(newest.date, datetime.datetime(2023, 4, 12))
            self.assertEqual(newest.source, root / 'entries/2023-04-12.html')
            self.assertEqual(newest.banner, 'test.jpg')
            self.assertEqual(newest.description, 'Test Entry 1')
            self.assertEqual(newest.page_next, '2021-01-01.html')
            self.assertEqual(newest.page_previous, None)

    def test_render_entry(self):
        page = unittest.mock.Mock(
            title='Some Test Page',
            description='Just a test page for the test suite',
            filename='test.html',
            banner='test.jpg',
            page_next=None,
            page_previous=None)

        content = '''
<p>This is some test conent.</p>

<figure>
  <a href="test.jpg">
    <img src="test.jpg" alt="test"/>
  </a>
</figure>'''.strip()

        actual = entries.render_entry(page,
                                      content=content,
                                      full_url='http://localhost:8080',
                                      year=1990,
                                      author='Joe Schmo')
        expected = '''
<!doctype html>
<html lang="en">

<head>
  <title>Some Test Page</title>

  <!-- Page Assets -->
  <link href="./favicon.ico" rel="shortcut icon" type="image/x-icon" />
  <link href="./assets/site.css" rel="stylesheet" />

  <!-- Page Metadata -->
  <meta charset="UTF-8" />
  <meta content="width=device-width, initial-scale=1" name="viewport" />
  <meta content="Some Test Page" name="twitter:title" />
  <meta content="Just a test page for the test suite" name="twitter:description" />
  <meta content="http://localhost:8080/test.html" name="og:url" />
  <meta content="article" property="og:type" />
  <meta content="Some Test Page" property="og:title" />
  <meta content="Just a test page for the test suite" property="og:description" />
  <meta content="http://localhost:8080/images/banners/test.jpg" name="og:image" />
  <meta content="http://localhost:8080/images/banners/test.jpg" name="twitter:image" />

</head>

<body>
  <article>

    <!-- Page Header -->
    <header>
      <h1>Some Test Page</h1>
      <p>Just a test page for the test suite</p>
    </header>

    <hr />

    <!-- Page Breadcrumbs -->
    <nav>
      <a href="./index.html">index.html</a>
      <span>/ test.html</span>
    </nav>

    <hr />

    <!-- Page Banner -->
    <figure>
      <a href="./images/banners/test.jpg">
        <img alt="page banner" src="./images/banners/test.jpg" />
      </a>
    </figure>

    <!-- Begin Page Content -->
    <p>This is some test conent.</p>

    <figure>
      <a href="test.jpg">
        <img src="test.jpg" alt="test"/>
      </a>
    </figure>
    <!-- End Page Content -->

  </article>

  <hr />

  <!-- Page Footer -->
  <footer>
    <small>© Copyright 1990 Joe Schmo</small>
  </footer>

</body>

</html>
'''.lstrip()
        self.assertEqual(actual, expected)

        entry = unittest.mock.Mock(
            title='Some Test Page',
            description='Just a test page for the test suite',
            filename='test.html',
            banner='test.jpg',
            page_next='next-page.html',
            page_previous='previous-page.html')

        actual = entries.render_entry(entry,
                                      full_url='http://localhost:8000',
                                      author='Alex',
                                      year=1990)
        self.assertIn(
            '''
    <!-- Pagination -->
    <nav>
      <a href="./previous-page.html">⟵ previous-page.html</a>
      &nbsp
      <a href="./next-page.html">next-page.html ⟶</a>
    </nav>
''', actual)

    def test_write_entries(self):
        entry = unittest.mock.Mock(
            title='Some Test Page',
            description='Just a test page for the test suite',
            filename='test.html',
            banner='test.jpg',
            page_next='next-page.html',
            page_previous='previous-page.html')
        with temp_root() as d:
            with (d / 'entries/test.html').open('w') as f:
                f.write('Test content!')

            entry.source = d / 'entries/test.html'
            entries.write_entries([entry] * 101,
                                  d / 'www',
                                  full_url='http://biz.local',
                                  author='Bill S. Preston',
                                  year='1988')
            with (d / 'www/test.html').open('r') as f:
                content = f.read()
                self.assertIn('<title>Some Test Page</title>', content)
