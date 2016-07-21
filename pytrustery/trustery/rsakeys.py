"""Functions for processing RSA keys."""
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


def new_key():
    """Create a new key."""
    return RSA.generate(2048)


def get_fingerprint(key):
    """
    Get the fingerprint of a key.

    key: the RSA key object.

    Returns the fingerprint string.
    """
    return SHA256.new(key.publickey().exportKey(format='DER')).hexdigest()
