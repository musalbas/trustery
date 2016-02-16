import os

from appdirs import user_config_dir
from configobj import ConfigObj

configfile = os.path.join(user_config_dir('trustery'), 'config.ini')
userconfig = ConfigObj(configfile)
