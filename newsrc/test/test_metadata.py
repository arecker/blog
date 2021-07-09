import unittest

from newsrc.metadata import parse_metadata


class MetadataTestCase(unittest.TestCase):
    def test_parse_metadata(self):
        content = '''

<!-- metadata:title: party, dumplings, and blogging -->

Dear Journal,

I had such a productive day yesterday. Nothing feels as good as putting
together a to-do list and actually finishing it before the day is done.
We're in full party planning mode for Rodney's birthday this weekend. I
think we'll have fewer people this year, but something tells me it will
still be a really good time. Smaller parties can be more fun - certainly
for me, as that would mean I just do less floating around.
'''.lstrip()

        actual = parse_metadata(content)

        self.assertDictEqual(actual, {
            'title': 'party, dumplings, and blogging'
        })

        content = '''
---
title: party, dumplings, and blogging
---

Dear Journal,

I had such a productive day yesterday. Nothing feels as good as putting
together a to-do list and actually finishing it before the day is done.
We're in full party planning mode for Rodney's birthday this weekend. I
think we'll have fewer people this year, but something tells me it will
still be a really good time. Smaller parties can be more fun - certainly
for me, as that would mean I just do less floating around.
'''.lstrip()

        actualData, actualLeftovers = parse_metadata(content, legacy=True)

        self.assertDictEqual(actualData, {
            'title': 'party, dumplings, and blogging'
        })

        self.assertEqual(actualLeftovers, '''
Dear Journal,

I had such a productive day yesterday. Nothing feels as good as putting
together a to-do list and actually finishing it before the day is done.
We're in full party planning mode for Rodney's birthday this weekend. I
think we'll have fewer people this year, but something tells me it will
still be a really good time. Smaller parties can be more fun - certainly
for me, as that would mean I just do less floating around.
''')
