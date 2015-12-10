#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Configurations """

import os
import json

#######################
# Warning: this decides about final configuration
PATH = 'angular'   # Main directory where all conf files are found
# Warning: this decides about final configuration
#######################

CONFIG_PATH = 'config'
JSON_EXT = 'json'


########################################
# Read user config
def read_files(path):
    """ All user specifications """
    sections = ['content', 'models', 'options']
    myjson = {}
    for section in sections:
        filename = os.path.join(CONFIG_PATH, path, section + "." + JSON_EXT)
        with open(filename) as f:
            myjson[section] = json.load(f)
    return myjson

# Use the function
user_config = read_files(PATH)


########################################
class BaseConfig(object):

    DEBUG = os.environ.get('APP_DEBUG', False)
    TESTING = False
    MYCONFIG_PATH = os.path.join(CONFIG_PATH, PATH)

    SECRET_KEY = 'my precious'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOST = 'localhost'
    PORT = int(os.environ.get('PORT', 5000))

    BASIC_USER = {
        'username': user_config['content'].get('username', 'prototype'),
        'password': user_config['content'].get('password', 'test'),
        'email': user_config['content'].get('email', 'idonotexist@test.com')
    }
