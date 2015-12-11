#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Factory and blueprints patterns """

import os
import logging
from .meta import Meta as m

################
config = {
    "default": "config.devel",
    "development": "config.devel",
    "production": "config.prod",
    # "testing": "bookshelf.config.TestingConfig",
}
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
CONFIG_MODULE = config[config_name]
configuration_module = m().get_module_from_string(CONFIG_MODULE)

print("Configuration:\t%s in [%s]" % (config_name, CONFIG_MODULE))
print(configuration_module)

################
# LOGGING
if configuration_module.MyConfig.DEBUG:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# String for formatting logs
FORMAT = '%(asctime)-15s [%(name)-8s|%(levelname)-8s] %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)
# Create logger
logging.getLogger(__name__).addHandler(NullHandler())


def get_logger(name):
    """ Recover the right logger + set a proper specific level """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    return logger
