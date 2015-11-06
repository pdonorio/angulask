#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Flask application main file """

# Import app factory
from app import create_app
# Choose configuration
from config import DevelopmentConfig
# Create the flask application object
app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    host = app.config.get("HOST")
    port = app.config.get("PORT")
    app.run(host=host, port=port)
