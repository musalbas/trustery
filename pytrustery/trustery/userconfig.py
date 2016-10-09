"""Local user configuration management."""

import os

from appdirs import user_config_dir
from configobj import ConfigObj

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
