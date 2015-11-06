#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Configurations """

import os
import json

########################################

#######################
# Warning: this decides about final configuration
PATH = 'base'   # Main directory where all conf files are found
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

    DEBUG = False
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


class DevelopmentConfig(BaseConfig):

    DEBUG = True
    HOST = '0.0.0.0'
    WTF_CSRF_SECRET_KEY = 'a random string'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    # # We have POSTGRESQL. Use docker environment variables
    # dbdriver = "postgresql"
    # dbhost = os.environ["DB_NAME"].split('/')[2]
    # dbport = int(os.environ["DB_PORT"].split(':')[2])
    # dbuser = os.environ["DB_ENV_POSTGRES_USER"]
    # dbpw = os.environ["DB_ENV_POSTGRES_PASSWORD"]
    # database = os.environ["DB_ENV_POSTGRES_DB"]

    # SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%d/%s" \
    #     % (dbdriver, dbuser, dbpw, dbhost, dbport, database)
