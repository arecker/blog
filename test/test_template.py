import unittest

from src.media import Image
from src.template import embed


class TestEmbed(unittest.TestCase):
    def test_embed_image(self):
        img = Image('./www/images/hello.jpg')
        actual = embed(img)
        expected = '''
<figure>
  <a href="./images/hello.jpg">
    <img alt="Hello" src="./images/hello.jpg" />
  </a>
</figure>'''.lstrip()
        self.assertEqual(actual, expected)
