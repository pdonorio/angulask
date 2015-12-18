#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

import requests
import simplejson as json
from flask.ext.login import login_user
from .basemodel import User
from . import htmlcodes as hcodes

NODE = 'myapi'
PORT = 5000
URL = 'http://%s:%s' % (NODE, PORT)
LOGIN_URL = URL + '/api/login'
HEADERS = {'content-type': 'application/json'}


def login_api(username, password):
    """ Login requesting token to our API and also store the token """

    token = None
    payload = {'email': username, 'password': password}

    # http://mandarvaze.github.io/2015/01/token-auth-with-flask-security.html
    try:
        r = requests.post(LOGIN_URL,
                          data=json.dumps(payload), headers=HEADERS, timeout=5)
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to APIs server", token

    out = r.json()
    if 'response' not in out:
        return None, "Cannot understand response format", token

    if out['meta']['code'] > hcodes.HTTP_OK_NORESPONSE:
        mess = ""
        for key, value in out['response']['errors'].items():
            mess += key + ': ' + value.pop() + '<br>'
        return False, mess, token

    data = out['response']['user']
    token = data['authentication_token']
    registered_user = User.query.filter_by(id=data['id']).first()
    return True, registered_user, token


def login_internal(username, password):
    """ Login with internal db """
    last = None
    registered_user = \
        User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return False, "No such user/password inside DB", last
    return True, registered_user, last


def login_point(username, password):
    """ Handle all possible logins """
    # API
    if BACKEND:
        check, data, token = login_api(username, password)
###############
# // TO FIX:
# Save token
        if check:
            print("\n\nTOKEN\n\n", token)
###############
    # Standalone server
    else:
        check, data, token = login_internal(username, password)

    # Register positive response to Flask Login in both cases
    if check:
        login_user(data)

    # Return response
    return check, data
