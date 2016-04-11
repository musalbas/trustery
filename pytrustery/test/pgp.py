import pickle
import unittest

from trustery.events import Events


class TestPGP(unittest.TestCase):
    def test_verify_attribute_pgp_proof(self):
        events = Events()

        attribute = pickle.load(open('res/pgp_attribute_1.pickle'))
        valid = events.verify_attribute_pgp_proof(attribute)
        self.assertTrue(valid)

        attribute = pickle.load(open('res/pgp_attribute_2.pickle'))
        valid = events.verify_attribute_pgp_proof(attribute)
        self.assertIsNone(valid)

        attribute = pickle.load(open('res/pgp_attribute_3.pickle'))
        valid = events.verify_attribute_pgp_proof(attribute)
        self.assertFalse(valid)

if __name__ == '__main__':
    unittest.main()
