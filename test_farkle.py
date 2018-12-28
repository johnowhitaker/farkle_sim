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

    def test_unique(self):
        roll = [1, 2, 3, 4, 5, 6]
        self.assertEqual(roll, unique(roll))
        roll = [1, 3, 2, 5, 4, 6]
        self.assertEqual(roll, unique(roll))
        self.assertEqual(unique([1, 1, 1, 1, 1, 1]), [1])
        self.assertEqual(unique([1, 1, 1, 1, 1, 2]), [1, 2])
        self.assertEqual(unique([2, 1, 1, 1, 1, 1]), [2, 1])
        self.assertEqual(unique([2, 1, 1, 2, 1, 1]), [2, 1])

    def test_test_for_3oak(self):
        self.assertFalse(test_for_3oak([1, 3, 2, 5, 4, 6])[0])
        self.assertFalse(test_for_3oak([1, 3, 2, 3, 4, 6])[0])
        self.assertTrue(test_for_3oak([1, 3, 2, 3, 3, 6])[0])
        self.assertEqual(test_for_3oak([1, 3, 2, 3, 3, 6])[1], 3)

    def test_test_for_3pairs(self):
        self.assertFalse(test_for_3pairs([1, 3, 2, 5, 4, 6]))
        self.assertFalse(test_for_3pairs([1, 3, 2, 3, 4, 6]))
        self.assertTrue(test_for_3pairs([1, 3, 2, 2, 3, 1]))

    def test_test_for_23s(self):
        self.assertFalse(test_for_23s([1, 3, 2, 5, 4, 6]))
        self.assertFalse(test_for_23s([1, 3, 3, 3, 4, 6]))
        self.assertTrue(test_for_23s([1, 3, 1, 3, 3, 1]))

    def test_test_for_run(self):
        self.assertTrue(test_for_run([1, 3, 2, 4, 6, 5]))
        self.assertFalse(test_for_run([1, 2, 3, 3, 5, 6]))



if __name__ == '__main__':
    unittest.main()
