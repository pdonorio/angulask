#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Development configuration """

import os
from . import BaseConfig


class MyConfig(BaseConfig):

    HOST = '0.0.0.0'
    WTF_CSRF_SECRET_KEY = 'a random string'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    print("Development mode... Switching to sqllite.")
