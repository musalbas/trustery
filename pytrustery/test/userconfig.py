import unittest

from trustery.userconfig import *


class TestUserConfig(unittest.TestCase):
    def test_truststore(self):
        self.assertFalse(trusted('foo'))

        trust('foo')
        self.assertTrue(trusted('foo'))

        untrust('foo')
        self.assertFalse(trusted('foo'))

if __name__ == '__main__':
    unittest.main()
