import unittest
from main import handler


class HandlerTestCase(unittest.TestCase):
    def test_handler(self):
        self.assertEqual(handler(None, None), True)

if __name__ == '__main__':
    unittest.main()
