import unittest

from src.media import NewImage as Image


class TestImage(unittest.TestCase):
    def test_filename(self):
        self.assertEqual(Image('test.jpg').filename, 'test.jpg')
        self.assertEqual(Image('something/test.jpg').filename, 'test.jpg')

    def test_date_slug(self):
        actual = Image('1990-09-28-test.jpg').date_slug
        expected = '1990-09-28'
        self.assertEqual(actual, expected)

        actual = Image('banners/1990-09-28.jpg').date_slug
        expected = '1990-09-28'
        self.assertEqual(actual, expected)

        with self.assertRaises(ValueError):
            Image('banners/quotes.jpg').date_slug

    def test_date(self):
        actual = Image('1990-09-28-test.jpg').date
        actual = (actual.year, actual.month, actual.day)
        expected = (1990, 9, 28)
        self.assertEqual(actual, expected)

        with self.assertRaises(ValueError):
            Image('banners/quotes.jpg').date

    def test_slug(self):
        actual = Image('1990-09-28-test-image.jpg').slug
        expected = 'test-image'
        self.assertEqual(actual, expected)

        actual = Image('1990-09-28.jpg').slug
        self.assertIsNone(actual)

    def test_title(self):
        actual = Image('1990-09-28-test-image.jpg').title
        expected = 'Test Image'
        self.assertEqual(actual, expected)

    def test_href(self):
        actual = Image('www/images/test.jpg').href
        expected = './images/test.jpg'
        self.assertEqual(actual, expected)

        actual = Image('www/images/subfolder/test.jpg').href
        expected = './images/subfolder/test.jpg'
        self.assertEqual(actual, expected)

        actual = Image('./www/images/test.jpg').href
        expected = './images/test.jpg'
        self.assertEqual(actual, expected)
