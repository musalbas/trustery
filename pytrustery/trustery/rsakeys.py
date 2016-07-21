"""Functions for processing RSA keys."""
from Crypto.PublicKey import RSA


def new_key():
    """Create a new key."""
    return RSA.generate(2048)
