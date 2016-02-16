"""Local user configuration management."""

import os

from appdirs import user_config_dir
from configobj import ConfigObj

# Determine cross-platform configuration file path.
configfile = os.path.join(user_config_dir('trustery'), 'config.ini')

# Create configuration object.
userconfig = ConfigObj(configfile)
