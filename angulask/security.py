#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

import requests
import simplejson as json
from datetime import datetime
# from flask import Response, stream_with_context
from flask.ext.login import login_user, UserMixin
from config import BACKEND
from .basemodel import db, lm, User
from . import htmlcodes as hcodes

##################################
# If connected to APIs
if BACKEND:

    NODE = 'myapi'
    PORT = 5000
    URL = 'http://%s:%s' % (NODE, PORT)
    LOGIN_URL = URL + '/api/login'
    HEADERS = {'content-type': 'application/json'}

    @lm.user_loader
    def load_user(id):
        """ How Flask login can choose the current user. """
        return Tokenizer.query.get(id)

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

##################################
# If standalone db/auth/resources
else:
    @lm.user_loader
    def load_user(id):
        """ How Flask login can choose the current user. """
        return User.query.get(int(id))


##################################
def login_api(username, password):
    """ Login requesting token to our API and also store the token """

    payload = {'email': username, 'password': password}
    try:
        r = requests.post(LOGIN_URL, stream=True,
                          data=json.dumps(payload), headers=HEADERS, timeout=5)
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to APIs server"
    out = r.json()

    tokobj = None
    if out['meta']['code'] <= hcodes.HTTP_OK_NORESPONSE:
        data = out['response']['user']
        token = data['authentication_token']

        # Save token inside frontend db
        registered_user = User.query.filter_by(id=data['id']).first()
        tokobj = Tokenizer(token, registered_user.id)  # or data['id']
        db.session.add(tokobj)
        db.session.commit()

    # return True, tokobj
    return {'authentication_token':token}, out['meta']['code'], tokobj
    #return out['response'], out['meta']['code'], tokobj

    # # Stream original response as a proxy
    # return Response(
    #     stream_with_context(r.iter_content()),
    #     content_type=r.headers['content-type'])


def login_internal(username, password):
    """ Login with internal db """
    registered_user = \
        User.query.filter_by(username=username, password=password).first()

    data = {'errors': {'failed': "No such user/password inside DB"}}
    code = hcodes.HTTP_BAD_UNAUTHORIZED

    if registered_user is not None:
        data = {'user': {'id': registered_user.id}}
        code = hcodes.HTTP_OK_ACCEPTED

    return data, code, registered_user


def login_point(username, password):
    """ Handle all possible logins """

    # API
    if BACKEND:
        data, code, obj = login_api(username, password)
    # Standalone server
    else:
        data, code, obj = login_internal(username, password)
    # Register positive response to Flask Login in both cases
    if obj is not None:
        login_user(obj)
    # Return (forward) response
    return data, code
