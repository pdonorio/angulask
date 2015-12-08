#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Factory and blueprints patterns """

import os
import logging
import csv
from flask import Flask, request as req
from sqlalchemy import inspect
from .pages import cms
from .basemodel import db, lm, User, MyModel

config = {
    "default": "config.BaseConfig",
    "development": "config.devel.MyConfig",
    # "testing": "bookshelf.config.TestingConfig",
}


def init_insert(db, userconfig):
    # Add at least the first user
    user = User(**userconfig['BASIC_USER'])
    db.session.add(user)
    db.session.commit()

    # Try to populate with data if there is some
    modelname = 'mymodel'
    csvfile = os.path.join(userconfig['MYCONFIG_PATH'], modelname + '.csv')
    if not os.path.exists(csvfile):
        return

    data = []
    with open(csvfile, 'r') as csvfile:
        creader = csv.reader(csvfile, delimiter=';')
        for row in creader:
            data.append(row)

    mapper = inspect(MyModel)
    for pieces in data:
        i = 0
        content = {}
        for column in mapper.attrs:
            try:
                value = pieces[i]
                if not (value == '-' or value.strip() == ''):
                    content[column.key] = pieces[i]
            except:
                pass
            i += 1
        # Add one row at the time
        obj = MyModel(**content)
        db.session.add(obj)
    db.session.commit()


def create_app():
    """ Create the istance for Flask application """

    # Create a FLASK application
    app = Flask(__name__)  # , static_url_path='')
    # Note: since the app is defined inside this file,
    # the static dir will be searched inside this subdirectory

    # Apply configuration
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    print("Configuration:\t%s[%s]" % (config_name, config[config_name]))
    app.config.from_object(config[config_name])

    # # Cache
    # # http://flask.pocoo.org/docs/0.10/patterns/caching/#setting-up-a-cache
    # from werkzeug.contrib.cache import SimpleCache
    # cache = SimpleCache()

    # Database
    db.init_app(app)

    # Add things to this app
    app.register_blueprint(cms)
    app.logger.setLevel(logging.NOTSET)

    # Flask LOGIN
    lm.init_app(app)
    lm.login_view = '.login'

    # Application context
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
# // TO FIX:
# Drop tables and populate with basic data, only on request
# e.g. startup option
        db.drop_all()
        print("Created DB/tables")
        db.create_all()
        init_insert(db, app.config)

# SANITY CHECKS?
        # from .sanity_checks import is_sane_database
        # from .models import MyModel
        # # Note, this will check all models, not only MyModel...
        # is_sane_database(MyModel, db.session)

    # Logging
    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
                        req.method, req.url, req.data, resp))
        return resp

    return app
