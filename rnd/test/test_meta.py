import unittest

from blog.meta import descendants


class MetaTestCase(unittest.TestCase):
    def test_descendants(self):
        class Animal:
            pass

        class Dog(Animal):
            pass

        class Pig(Animal):
            pass

        class Corgi(Dog):
            pass

        actual = descendants(Animal)
        expected = [Dog, Pig, Corgi]

        self.assertCountEqual(actual, expected, 'should retrieve all subclasses')
