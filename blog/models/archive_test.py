import unittest
import datetime

from blog import html
from blog.models import Page, Site, Archive


class TestArchive(unittest.TestCase):
    def setUp(self):
        self.entries = [
            Page(source=f'{year}-01-01.html',
                 is_entry=True,
                 description=f'entry {year}',
                 banner=f'{year}-01-01.jpg')
            for year in (2018, 2019, 2020, 2021)
        ]
        self.entries += [
            Page(source=f'2021-0{month}-01.html',
                 is_entry=True,
                 description=f'entry 2021 {month}',
                 banner=f'2021-0{month}-01.jpg') for month in (2, 3, 4, 5)
        ]
        self.site = Site(directory='~/src/blog', entries=self.entries)
        self.archive = Archive(site=self.site)

    def test_repr(self):
        self.assertEqual(repr(self.archive), '<Archive ~/src/blog/entries/>')

    def test_list_years(self):
        self.assertEqual(self.archive.list_years(), [2021, 2020, 2019, 2018])

    def test_list_months(self):
        self.assertEqual(self.archive.list_months(2021), [5, 4, 3, 2, 1])

    def test_list_entries(self):
        entries = self.archive.list_entries(2021, 5)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].date,
                         datetime.datetime(year=2021, month=5, day=1))

    def test_pages(self):
        expected = [
            '2021.html',
            '2020.html',
            '2019.html',
            '2018.html',
        ]
        expected += [
            '2021-05.html', '2021-04.html', '2021-03.html', '2021-02.html',
            '2021-01.html', '2020-01.html', '2019-01.html', '2018-01.html'
        ]
        actual = list(self.archive.pages())
        self.assertEqual(sorted([p.filename for p in actual]),
                         sorted(expected))

        first = actual[0]
        self.assertEqual(first.title, '2021-05')
        self.assertEqual(first.description, 'All Entries from May 2021')

        last = actual[-1]
        self.assertEqual(last.title, '2018')
        self.assertEqual(last.description, 'All Entries from 2018')

    def test_build_year_page_data(self):
        actual = self.archive.build_year_page_data(2021)

        self.assertEqual(actual, [
            ['/2021-05.html', 1],
            ['/2021-04.html', 1],
            ['/2021-03.html', 1],
            ['/2021-02.html', 1],
            ['/2021-01.html', 1],
        ])

    def test_build_year_page_content(self):
        actual = self.archive.build_year_page_content(2021)
        actual = html.stringify_xml(actual)
        self.assertEqual(
            actual, '''
<table>
  <tr>
    <th>Month Index</th>
    <th>No. of Entries</th>
  </tr>
  <tr>
    <td>
      <a href="/2021-05.html">2021-05.html</a>
    </td>
    <td>1</td>
  </tr>
  <tr>
    <td>
      <a href="/2021-04.html">2021-04.html</a>
    </td>
    <td>1</td>
  </tr>
  <tr>
    <td>
      <a href="/2021-03.html">2021-03.html</a>
    </td>
    <td>1</td>
  </tr>
  <tr>
    <td>
      <a href="/2021-02.html">2021-02.html</a>
    </td>
    <td>1</td>
  </tr>
  <tr>
    <td>
      <a href="/2021-01.html">2021-01.html</a>
    </td>
    <td>1</td>
  </tr>
</table>
'''.strip())
