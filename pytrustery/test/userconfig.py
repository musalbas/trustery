import unittest

from trustery.userconfig import *


class TestUserConfig(unittest.TestCase):
    def test_truststore(self):
        self.assertFalse(is_trusted('foo'))

        trust('foo')
        self.assertTrue(is_trusted('foo'))

        untrust('foo')
        self.assertFalse(is_trusted('foo'))

if __name__ == '__main__':
    unittest.main()
