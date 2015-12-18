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

BACKEND = False
for key in os.environ.keys():
    if 'backend' in key.lower():
        BACKEND = True


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

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    BASE_DB_DIR = '/dbs'
    SQLLITE_DBFILE = 'frontend.db'
    dbfile = os.path.join(BASE_DB_DIR, SQLLITE_DBFILE)
    SECRET_KEY = 'my-super-secret-keyword_referringtofrontendside'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbfile
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my precious'

    HOST = 'localhost'
    PORT = int(os.environ.get('PORT', 5000))

    BASIC_USER = {
        'username': user_config['content'].get('username', 'prototype'),
        'password': user_config['content'].get('password', 'test'),
        'email': user_config['content'].get('email', 'idonotexist@test.com')
    }
