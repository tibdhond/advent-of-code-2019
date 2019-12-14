from day14.day14_script import *
import unittest


class Tests(unittest.TestCase):
    def test1(self):
        self.assertEqual(part1("test1.txt"), 31)

    def test2(self):
        self.assertEqual(part1("test2.txt"), 165)

    def test3(self):
        self.assertEqual(part1("test3.txt"), 13312)

    def test4(self):
        self.assertEqual(part1("test4.txt"), 180697)

    def test5(self):
        self.assertEqual(part1("test5.txt"), 2210736)


if __name__ == '__main__':
    unittest.main()
