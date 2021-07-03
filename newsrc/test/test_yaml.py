import unittest

from newsrc.yaml import parse_yaml


class YamlTestCase(unittest.TestCase):
    def test_parse_yaml(self):
        content = '''
title: the unit test
description: a story about the brave little unit test that could.
'''.lstrip()

        actual = parse_yaml(content)

        self.assertDictEqual(actual, {
            'title': 'the unit test',
            'description': 'a story about the brave little unit test that could.'
        })
