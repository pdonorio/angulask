#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Development configuration """

import os
from . import BaseConfig


class MyConfig(BaseConfig):

    DEBUG = True
    HOST = '0.0.0.0'
    WTF_CSRF_SECRET_KEY = 'a random string'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    try:
        # We have POSTGRESQL. Use docker environment variables
        dbhost = os.environ["DB_NAME"].split('/')[2]
        dbport = int(os.environ["DB_PORT"].split(':')[2])
        dbuser = os.environ["DB_ENV_POSTGRES_USER"]
        dbpw = os.environ["DB_ENV_POSTGRES_PASSWORD"]
        database = os.environ["DB_ENV_POSTGRES_DB"]
        dbdriver = "postgresql"

        SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%d/%s" \
            % (dbdriver, dbuser, dbpw, dbhost, dbport, database)
    except Exception:
        print("Cannot found a database instance. Switching to sqllite.")
        pass
