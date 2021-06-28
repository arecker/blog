import unittest

import lib as blog


class FrontmatterTestCase(unittest.TestCase):
    def test_parse_frontmatter(self):
        content = '''
---
title: Dear Journal
description: Daily, public journal by Alex Recker
---

<div class="row">
</div>
'''.lstrip()

        data, leftovers = blog.parse_frontmatter(content)

        expectedData = {
            'title': 'Dear Journal',
            'description': 'Daily, public journal by Alex Recker'
        }

        expectedLeftovers = '''
<div class="row">
</div>
'''.lstrip()

        self.assertDictEqual(data, expectedData)
        self.assertEqual(leftovers, expectedLeftovers)

        content = '''
Nothing to see here!
'''.lstrip()

        data, leftovers = blog.parse_frontmatter(content)

        self.assertDictEqual(data, {})
        self.assertEqual(leftovers, content)
