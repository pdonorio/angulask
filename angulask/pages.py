#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

import os
import glob
from pathlib import Path
from flask import Blueprint, current_app, \
    render_template, request, flash, redirect, url_for, abort, g
from flask.ext.login import logout_user, current_user, login_required
from werkzeug import secure_filename
from .basemodel import db, \
    create_table, Col, \
    MyModel, MyTable, \
    user_config, insertable, selected
from . import forms
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
    bowerdir + "animate.css/animate.min.css",
    staticdir + "css/custom.css"
]
############################

# Angular framework and app files
js = [
    bowerdir + "angular/angular.min.js",
    bowerdir + "angular-animate/angular-animate.min.js",
    bowerdir + "angular-cookies/angular-cookies.min.js",
    bowerdir + "angular-sanitize/angular-sanitize.min.js",
    bowerdir + "angular-ui-router/release/angular-ui-router.min.js",
    bowerdir + "lodash/lodash.min.js",
    bowerdir + "restangular/dist/restangular.min.js",
    bowerdir + "angular-strap/dist/angular-strap.min.js",
    bowerdir + "angular-strap/dist/angular-strap.tpl.min.js",
    bowerdir + "moment/min/moment.min.js",
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
    return render_template(template_path + '/' + page, **tmp)


#################################
# BASIC INTERFACE ROUTES
@cms.route('/')
@cms.route('/home')
def home():
    return templating('pages/placeholder.home.html')


@cms.route('/about')
def about():
    return templating('pages/placeholder.about.html')


#################################
def single_element_insert_db(iform, obj):
    iform.populate_obj(obj)
# // TO FIX:
# Does not work as autoincrement
    # Id is supposed to exist, and also be autoincrement:
    obj.id = ''
    db.session.add(obj)
    db.session.commit()


def row2dict(r):
    """ Convert a single sqlalchemy row into a dictionary """
    # http://stackoverflow.com/a/1960546/2114395
    return {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


######################################################
@cms.route('/view', methods=["GET", "POST"])
@cms.route('/view/<int:id>', methods=["GET"])
@login_required
def view(id=None):
    status = "View"
    template = 'forms/view.html'
    mytable = None

    # SORT
    sort_field = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    field = getattr(MyModel, sort_field)
    if reverse:
        from sqlalchemy import desc
        field = desc(field)

    ####################################################
    # SINGLE VIEW
    if id is not None:
        template = 'forms/singleview.html'
        status = 'Single ' + status + \
            sort_field + ' for Record <b>#' + str(id) + '</b>'
        items = [MyModel.query.filter(
            MyModel.id == id).first()._asdict()]
        # Upload
        uploaded = request.args.get('uploaded')
        if uploaded is not None:
            flash("Uploaded file '%s'" % uploaded, 'success')
        # List of available files
        ufolder = current_app.config['UPLOAD_FOLDER']
        mydir = os.path.join(ufolder, str(id)) + '/'
        flist = glob.glob(mydir + '*')
        if flist:
            TableCls = create_table("file_list")
            TableCls.add_column('files', Col('Already associated files:'))
            TableCls.classes = ['table', 'table-hover']
            tcontent = []
            for f in flist:
                tcontent.append({'files': f.replace(mydir, '')})
            mytable = TableCls(tcontent)

    # SINGLE VIEW
    ####################################################

    ####################################################
    # NORMAL VIEW (all elements)
    else:
        # SQLalchemy query (sorted)
        data = MyModel.query.order_by(field)
        items = []
        for row in data:
            pieces = row2dict(row)
            final = {}
            for key, value in pieces.items():
                if key in selected:
                    final[key] = value
            items.append(final)
    # NORMAL VIEW (all elements)
    ####################################################

    return templating(
        template, ftable=mytable,
        table=MyTable(items, sort_by=sort_field, sort_reverse=reverse),
        status=status, formname='view', dbitems=items, id=id)


template = 'forms/insert_search.html'


@cms.route('/insert', methods=["GET", "POST"])
def insert():
    status = "Waiting data to save"
    iform = forms.DataForm()
    if iform.validate_on_submit():
        # Handle user model
        single_element_insert_db(iform, MyModel())
        flash("User saved", 'success')
        status = "Saved"

    return templating(template,
        status=status, form=iform, formname='insert', selected=insertable,
        keyfield =user_config['models'].get('key_field'))


@cms.route('/search', methods=["GET", "POST"])
def search():
    status = "Waiting data to search"
    iform = forms.DataForm()
    if iform.validate_on_submit():
        status = "Work in progress"
        # flash("User saved", 'success')
    return templating(
        template, status=status, form=iform, formname='search')


###########################################################
# LOGIN!
###########################################################

@cms.before_request
def before_request():
    """ Save the current user as the global user for each request """
    g.user = current_user


@cms.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return templating('forms/newlogin.html')

    check_auth, response = login_point(
            request.form['username'], request.form['password'])

    if check_auth is None:
        flash(response, 'danger')
        return templating('errors/500.html')
    elif check_auth:
        flash('Logged in successfully', 'success')

        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        next = request.args.get('next')
# //TO FIX: write next_is_valid..?
        #if not next_is_valid(next):
        if False:
            return abort(hcodes.HTTP_BAD_NOTFOUND)

        return redirect(next or url_for('pages.home'))

    flash('Username or Password is invalid', 'danger')
    print("FAILED LOGIN", response)
    return redirect(url_for('.login'))

# @cms.route('/testlogin')
# @login_required
# def testlogin(id=None):
#     flash("it works...")
#     return templating('main.html')

################################################
# # REIMPLEMENT
# @cms.route('/register')
# def register():
#     form = forms.RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)


# @cms.route('/forgot')
# def forgot():
#     form = forms.ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

@cms.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.home'))
################################################


################
# UPLOADs
################

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

# Only needed for separate debug

# # Route that will process the file upload
# @cms.route('/uploader/<int:id>', methods=['GET'])
# def uploader(id):
#     flash("Id is %d" % id)
#     return render_template('forms/upload.html', **user_config['content'])

# # Expecting a parameter containing the name of a file.
# # It will locate that file on the upload directory and show it
# @cms.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(current_app.config['UPLOAD_FOLDER'],
#                                filename)


# Route that will process the file upload
@cms.route('/upload/<int:id>', methods=['POST'])
def upload(id):
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Build the directory and make if if not exists
        mydir = os.path.join(
            current_app.config['UPLOAD_FOLDER'], str(id))
        if not os.path.exists(mydir):
            os.mkdir(mydir)
        abs_filepath = os.path.join(mydir, filename)
        # Move the file from the temporal folder
        file.save(abs_filepath)
        # Redirect
        # return redirect(url_for('.uploaded_file', filename=filename))
# // TO FIX:
# Change this to view of single id
        return redirect('/view/' + str(id) + '?uploaded=' + filename)


######################################################
myroute = 'angular'


@cms.route('/' + myroute + '/', methods=["GET", "POST"])
@cms.route('/' + myroute + '/<path:mypath>', methods=["GET", "POST"])
@login_required
def angular(mypath=None):
    template = 'angularviews/experiment.html'

############################
# Dirty fix for URL BASE in angular HTML5mode

    if request.url_root not in user_config['content']['stylesheets'][0]:
        # FIX CSS
        new = []
        tmp = user_config['content']['stylesheets']
        for x in tmp:
            new.append(request.url_root + x)
        user_config['content']['stylesheets'] = new
        # FIX JS
        new = []
        tmp = user_config['content']['jsfiles']
        for x in tmp:
            new.append(request.url_root + x)
        user_config['content']['jsfiles'] = new
        # FIX IMAGES
        new = []
        tmp = user_config['content']['logos']
        for x in tmp:
            new.append({
                'src': request.url_root + x['src'],
                'width': x['width']})
        user_config['content']['logos'] = new

# Dirty fix for URL BASE in angular HTML5mode
############################

    return render_template(template, mydomain='/' + myroute + '/',
                           **user_config['content'])
