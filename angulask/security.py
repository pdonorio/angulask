#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

import requests
import simplejson as json
from flask.ext.login import login_user, UserMixin
from datetime import datetime
from config import BACKEND
from .basemodel import db, lm, User
from . import htmlcodes as hcodes

NODE = 'myapi'
PORT = 5000
URL = 'http://%s:%s' % (NODE, PORT)
LOGIN_URL = URL + '/api/login'
HEADERS = {'content-type': 'application/json'}


class Tokenizer(db.Model, UserMixin):
    __tablename__ = "tokens"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, index=True)
    user_id = db.Column(db.Integer)
    authenticated_at = db.Column(db.DateTime)

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id
        self.authenticated_at = datetime.utcnow()

    def __repr__(self):
        return '<Tok for user[%r]> %s' % (self.user_id, self.token)


def login_api(username, password):
    """ Login requesting token to our API and also store the token """

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

    data = out['response']['user']
    token = data['authentication_token']

    # Save token inside frontend db
    registered_user = User.query.filter_by(id=data['id']).first()
    tok = Tokenizer(token, registered_user.id)  # or data['id']
    db.session.add(tok)
    db.session.commit()

    return True, tok


def login_internal(username, password):
    """ Login with internal db """
    registered_user = \
        User.query.filter_by(username=username, password=password).first()
    if registered_user is None:
        return False, "No such user/password inside DB"
    return True, registered_user


def login_point(username, password):
    """ Handle all possible logins """
    # API
    if BACKEND:
        check, data = login_api(username, password)
    # Standalone server
    else:
        check, data = login_internal(username, password)

    # Register positive response to Flask Login in both cases
    if check:
        login_user(data)

    # Return response
    return check, data


if BACKEND:
    @lm.user_loader
    def load_user(id):
        """ How Flask login can choose the current user. """
        return Tokenizer.query.get(id)
else:
    @lm.user_loader
    def load_user(id):
        """ How Flask login can choose the current user. """
        return User.query.get(int(id))
