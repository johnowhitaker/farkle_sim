import unittest
from farkle import *

# The demo example
class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class TestSupportMethods(unittest.TestCase):

    # def setUp(self): # Gets run before every test
    #     self.widget = Widget('The widget')

    def test_dice(self):
        d = dice(100)
        self.assertEqual(min(d), 1)
        self.assertEqual(max(d), 6)
        self.assertEqual(type(d[0]), int)


if __name__ == '__main__':
    unittest.main()
