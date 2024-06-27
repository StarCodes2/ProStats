#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.repository import Repository
from models.user import User
from os import environ
from flask import Flask, render_template, request, redirect, make_response, url_for
from flask_login import LoginManager, login_required, current_user
from hashlib import md5
from web.views import app_views
app = Flask(__name__)
app.secret_key = '2K24_06_shared_key'
app.register_blueprint(app_views)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

login_manager = LoginManager()
login_manager.init_app(app)
"""login_manager.id_attribute = 'get_id'"""
login_manager.login_view = 'app_views.login'


@login_manager.user_loader
def load_user(user_id):
    """ Loads the current user """
    for user in storage.all(User).values():
        if user_id == user.id:
            return user
    return None


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error handler """
    return make_response('Page not found', 404)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
