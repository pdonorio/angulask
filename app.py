#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Flask application main file """

# Import app factory
from angulask import create_app
# Configuration is decided via environment variable: FLASK_CONFIGURATION

if __name__ == '__main__':
    app = create_app()
    host = app.config.get("HOST")
    port = app.config.get("PORT")
    app.run(host=host, port=port)
