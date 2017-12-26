import unittest
import src.hello


class HelloTestCase(unittest.TestCase):
    def setUp(self):
        self.hello = src.hello.Hello()

    def test_(self):
        self.assertEqual(self.hello.message(), 'Hello, world!')

if __name__ == '__main__':
    unittest.main()
