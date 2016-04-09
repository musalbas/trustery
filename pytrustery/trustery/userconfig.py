"""Local user configuration management."""

import os

from appdirs import user_config_dir
from configobj import ConfigObj

# Determine cross-platform configuration file path.
configfile = os.path.join(user_config_dir('trustery'), 'config.ini')

# Create configuration object.
userconfig = ConfigObj(configfile)

# Initialise configuration.
if 'truststore' not in userconfig:
    userconfig['truststore'] = {}


def trust(address):
    """Add address to the trust store."""
    userconfig['truststore'][address] = True


def untrust(address):
    """Remove address from the trust store."""
    userconfig['truststore'][address] = False


def is_trusted(address):
    """Return True if an address is in the trust store, otherwise False."""
    return address in userconfig['truststore'] and userconfig['truststore'][address]


def get_trusted():
    """Return a list of trusted Ethereum addresses."""
    return userconfig['trustore'].keys()
