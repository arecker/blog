import unittest
import doctest

import src.feed
import src.media


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(src.feed))
    tests.addTests(doctest.DocTestSuite(src.media))
    return tests
