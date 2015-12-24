#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

from pathlib import Path

from flask import Blueprint, current_app, \
    render_template, request, flash, redirect, url_for, jsonify, g
from flask.ext.login import logout_user, current_user, login_required
#from werkzeug import secure_filename

from .basemodel import db, user_config
from .security import login_point
from . import htmlcodes as hcodes

# Blueprint for base pages, if any
cms = Blueprint('pages', __name__)

# Static things
staticdir = 'static/'
bowerdir = staticdir + 'bower/'

############################
# // TO FIX:
# ## This should depend on the chosen framework:
# ## Bootstrap, Foundation or Material

# CSS files
css = [
    bowerdir + "font-awesome/css/font-awesome.min.css",
    bowerdir + "bootstrap/dist/css/bootstrap.min.css",
    bowerdir + "angular-loading-bar/build/loading-bar.min.css",
    # bowerdir + "animate.css/animate.min.css",
    staticdir + "css/custom.css"
]
############################

# // TO FIX READ FROM JSON

# Angular framework and app files
js = [
    bowerdir + "angular/angular.min.js",
    # bowerdir + "angular-route/angular-route.min.js",
    bowerdir + "angular-ui-router/release/angular-ui-router.min.js",
    # bowerdir + "angular-strap/dist/angular-strap.min.js",
    # bowerdir + "angular-strap/dist/angular-strap.tpl.min.js",
    # bowerdir + "angular-animate/angular-animate.min.js",
    bowerdir + "angular-sanitize/angular-sanitize.min.js",
    bowerdir + "satellizer/satellizer.min.js",
    bowerdir + "angular-loading-bar/build/loading-bar.min.js",
# JWT ?

# Bower libs on demand
    # bowerdir + "moment/min/moment.min.js",
    # Force order: the angularjs app declaration should be the first
    staticdir + "app/app.js",
]

# Images
if 'logos' not in user_config['content']:
    user_config['content']['logos'] = [{
        "src": "static/img/default.png", "width": '90'
    }]

############################
# // TO FIX:
# ## This should load only a specified angular blueprint

# Dynamically load all other angularjs files
prefix = __package__
for pathfile in Path(prefix + '/' + staticdir + '/app').glob('**/*.js'):
    strfile = str(pathfile)
    jfile = strfile[len(prefix)+1:]
    if jfile not in js:
        js.append(jfile)
# // TO FIX -END
############################

user_config['content']['stylesheets'] = css
user_config['content']['jsfiles'] = js


def templating(page, framework='bootstrap', **whatever):
    template_path = 'frameworks' + '/' + framework
    tmp = whatever.copy()
    tmp.update(user_config['content'])
    templ = template_path + '/' + page
    print("TEST!\n\n", templ, tmp)
    return render_template(templ, **tmp)


def jstemplate(title='App', mydomain='/'):
    """ If you decide a different domain, use slash as end path,
        e.g. /app/ """
    return templating('enable_angular.html', mydomain=mydomain, jstitle=title)


# #################################
# # BASIC INTERFACE ROUTES
@cms.before_request
def before_request():
    """ Save the current user as the global user for each request """
    g.user = current_user


@cms.route('/helloworld')
def home():
    return templating('welcome.html')


@cms.route('/auth', methods=['POST'])
def auth():
    # Verify POST data
    if not ('username' in request.json and 'password' in request.json):
        return "No valid (json) data credentials", hcodes.HTTP_BAD_UNAUTHORIZED
    # Request login (with or without API)
    resp, code = login_point(
            request.json['username'], request.json['password'])
    if resp is None:
        resp = {}
    # Forward response
    return jsonify(**resp), code


@cms.route('/register')
def register():
    return "THIS IS YET TO DO (also 'forgot password')"


@cms.route('/felogout')
def fe_logout():
    logout_user()
    return redirect(url_for('.home'))
################################################


# ################
# # UPLOADs
# ################

# # For a given file, return whether it's an allowed type or not
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in \
#            current_app.config['ALLOWED_EXTENSIONS']

# # Only needed for separate debug

# # # Route that will process the file upload
# # @cms.route('/uploader/<int:id>', methods=['GET'])
# # def uploader(id):
# #     flash("Id is %d" % id)
# #     return render_template('forms/upload.html', **user_config['content'])

# # # Expecting a parameter containing the name of a file.
# # # It will locate that file on the upload directory and show it
# # @cms.route('/uploads/<filename>')
# # def uploaded_file(filename):
# #     return send_from_directory(current_app.config['UPLOAD_FOLDER'],
# #                                filename)


# # Route that will process the file upload
# @cms.route('/upload/<int:id>', methods=['POST'])
# def upload(id):
#     # Get the name of the uploaded file
#     file = request.files['file']
#     # Check if the file is one of the allowed types/extensions
#     if file and allowed_file(file.filename):
#         # Make the filename safe, remove unsupported chars
#         filename = secure_filename(file.filename)
#         # Build the directory and make if if not exists
#         mydir = os.path.join(
#             current_app.config['UPLOAD_FOLDER'], str(id))
#         if not os.path.exists(mydir):
#             os.mkdir(mydir)
#         abs_filepath = os.path.join(mydir, filename)
#         # Move the file from the temporal folder
#         file.save(abs_filepath)
#         # Redirect
#         # return redirect(url_for('.uploaded_file', filename=filename))
# # // TO FIX:
# # Change this to view of single id
#         return redirect('/view/' + str(id) + '?uploaded=' + filename)


######################################################
@cms.route('/', methods=["GET", "POST"])
@cms.route('/<path:mypath>', methods=["GET", "POST"])
# @login_required
def angular(mypath=None):
    return jstemplate()

# ############################
# # Dirty fix for URL BASE in angular HTML5mode

#     if request.url_root not in user_config['content']['stylesheets'][0]:
#         # FIX CSS
#         new = []
#         tmp = user_config['content']['stylesheets']
#         for x in tmp:
#             new.append(request.url_root + x)
#         user_config['content']['stylesheets'] = new
#         # FIX JS
#         new = []
#         tmp = user_config['content']['jsfiles']
#         for x in tmp:
#             new.append(request.url_root + x)
#         user_config['content']['jsfiles'] = new
#         # FIX IMAGES
#         new = []
#         tmp = user_config['content']['logos']
#         for x in tmp:
#             new.append({
#                 'src': request.url_root + x['src'],
#                 'width': x['width']})
#         user_config['content']['logos'] = new

# # Dirty fix for URL BASE in angular HTML5mode
# ############################
