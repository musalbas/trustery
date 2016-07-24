"""Functions for processing RSA keys."""
import base64
from random import SystemRandom

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


def generate_blinded_key_data(key, signingkey):
    """
    Generated a blinded RSA key to be signed.

    key: the RSA key object.
    signingkey: the RSA key object of the signing authority.

    Returns tuple (data representing a blinded RSA key ready for signing, blinding factor).
    """
    # Generate blinding factor.
    r = SystemRandom().randrange(signingkey.n >> 10, signingkey.n)

    # Generate unblinded message and hash.
    message = key.publickey().exportKey(format='DER')
    message = SHA256.new(message).digest()

    # Blind message.
    message = signingkey.blind(message, r)
    message = base64.b64encode(message)

    return (message, r)


def sign_blinded_key(keydata, signingkey):
    """
    Sign a blinded RSA key.

    keydata: the blinded RSA key data.
    signingkey: the RSA key object of the signing authority.

    Returns the signature.
    """
    rawblindedkey = base64.b64decode(keydata)
    signature = signingkey.sign(rawblindedkey, 0)[0]
    signature = hex(signature)[2:-1].decode('hex')
    signature = base64.b64encode(signature)

    return signature

def unblind_signature(signature, blindingfactor, signingkey):
    """
    Unblind a blind RSA signature.

    signature: the blind signature.
    blindingfactor: the blinding factor.
    """
    signature = base64.b64decode(signature)
    signature = long(signature.encode('hex'), 16)

    unblindedsignature = signingkey.unblind(signature, blindingfactor)
    unblindedsignature = hex(unblindedsignature)[2:-1].decode('hex')
    unblindedsignature = base64.b64encode(unblindedsignature)

    return unblindedsignature
