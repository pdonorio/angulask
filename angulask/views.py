#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rest view implementation
"""

from __future__ import absolute_import
import htmlcodes as hc
from flask import Blueprint, render_template, make_response
from jinja2 import TemplateNotFound
from flask_restful import Api, Resource


#########################
# Use restful plugin
def generate_blueprint(name='someviews', folder='templates', classes=[]):
    """ Using restful blueprint for all classes """
    # Add resources
    bp = Blueprint(name, __name__, template_folder=folder)
    rest = Api(bp)
    for view in classes:
        print("TEST CLASS", view)
        rest.add_resource(view, view().endpoint())
    return bp


class RestView(Resource):
    """ A base REST resource for views """
    _headers = {'Content-Type': 'text/html'}
    _endpoint = 'test'

    def __init__(self):
        """ Skip normal REST init """
        pass

    def endpoint(self):
        """ Define endpoint name based on class name """
        return '/' + self.__class__.__name__.lower()

    def render(self, page='test.html'):
        """ Render a python template as HTML page """
        try:
            return make_response(render_template(page),
                                 hc.HTTP_OK_BASIC, self._headers)
        except TemplateNotFound:
            return make_response("Failed",
                                 hc.HTTP_BAD_NOTFOUND, self._headers)
