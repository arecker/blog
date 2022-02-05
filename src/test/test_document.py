import unittest

from .. import Document


class TestDocument(unittest.TestCase):
    def test_render_head(self):
        actual = Document(
            title="Test Page",
            description="This is a test page."
        ).render_head()

        expected = """
<head>
  <title>Test Page</title>
  <link rel="shortcut icon" type="image/x-icon" href="./favicon.ico">
  <link href="./assets/site.css" rel="stylesheet">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="twitter:title" content="Test Page">
  <meta name="twitter:description" content="This is a test page.">
  <meta property="og:url" content="">
  <meta property="og:type" content="article">
  <meta property="og:title" content="Test Page">
  <meta property="og:description" content="This is a test page.">
  <meta name="image" content="">
  <meta property="og:image" content="">
</head>
""".strip()

        self.assertEqual(actual, expected)
