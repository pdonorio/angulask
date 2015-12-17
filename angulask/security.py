#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

import requests
import simplejson as json
from .basemodel import User
from flask.ext.login import login_user
from . import htmlcodes as hcodes

NODE = 'myapi'
PORT = 5000
URL = 'http://%s:%s' % (NODE, PORT)
LOGIN_URL = URL + '/api/login'
HEADERS = {'content-type': 'application/json'}


def login_api(username, password):
    """ Login with API and also store the token """
    payload = {'email': username, 'password': password}

    # http://mandarvaze.github.io/2015/01/token-auth-with-flask-security.html
    try:
        r = requests.post(LOGIN_URL,
                          data=json.dumps(payload), headers=HEADERS, timeout=5)
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to APIs server"

    out = r.json()
    if 'response' not in out:
        return None, "Cannot understand response format"

    if out['meta']['code'] > hcodes.HTTP_OK_NORESPONSE:
        mess = ""
        for key, value in out['response']['errors'].items():
            mess += key + ': ' + value.pop() + '<br>'
        return False, mess

    return True, out['response']['user']


def login_internal(username, password):

    registered_user = \
        User.query.filter_by(username=username, password=password).first()

    if registered_user is None:
        return False
    login_user(registered_user)
    return True


def login_point(username, password, backend):
    if backend:
        return login_api(username, password)
    return login_internal(username, password)
