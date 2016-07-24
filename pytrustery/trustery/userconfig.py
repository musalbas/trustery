"""Local user configuration management."""

import os

from appdirs import user_config_dir
from configobj import ConfigObj
from Crypto.PublicKey import RSA

from trustery import rsakeys

# Create configuration directory in case it does not exist.
try:
    os.makedirs(user_config_dir('trustery'))
except OSError:
    if not os.path.isdir(user_config_dir('trustery')):
        raise

# Determine cross-platform configuration file path.
configfile = os.path.join(user_config_dir('trustery'), 'config.ini')

# Create configuration object.
config = ConfigObj(configfile)

# Initialise configuration.
if 'truststore' not in config:
    config['truststore'] = {}
if 'rsa_keys' not in config:
    config['rsa_keys'] = {}
if 'rsa_blinded_keys' not in config:
    config['rsa_blinded_keys'] = {}


def trust(address):
    """
    Add address to the trust store.

    address: the address to add.
    """
    config['truststore'][address] = True


def untrust(address):
    """
    Remove address from the trust store.

    address: the address to remove.
    """
    del config['truststore'][address]


def is_trusted(address):
    """
    Return True if an address is in the trust store, otherwise False.

    address: the address to check.
    """
    return address in config['truststore'] and config['truststore'][address]


def get_trusted():
    """Return a list of trusted Ethereum addresses."""
    return config['truststore'].keys()


def add_rsa_key(privkey):
    """
    Add an RSA key to the configuration.

    privkey: an RSA key object containing a private key.

    Returns the fingerprint of the key.
    """
    fingerprint = rsakeys.get_fingerprint(privkey)
    config['rsa_keys'][fingerprint] = privkey.exportKey()
    return fingerprint


def load_rsa_key(fingerprint):
    """
    Load a stored RSA key.

    keyid: the fingerprint of the key.

    Returns an RSA key object.
    """
    return RSA.importKey(config['rsa_keys'][fingerprint])


def get_rsa_fingerprints():
    """Return a list of fingerprints of stored RSA keys."""
    return config['rsa_keys'].keys()


def add_rsa_blinded_key_data(blindedkey, r):
    """
    Store RSA blinded key data.

    blindedkey: the data representing the blinded key.
    r: the blinding factor.
    """
    blindedkey = blindedkey.replace('=', '-')
    config['rsa_blinded_keys'][blindedkey] = r


def get_rsa_blinding_factor(blindedkey):
    """
    Get a blinded key's blinding factor.

    blindedkey: the data representing the blinded key.

    Returns the blinding factor.
    """
    blindedkey = blindedkey.replace('=', '-')
    return int(config['rsa_blinded_keys'][blindedkey])
