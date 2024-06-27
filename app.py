#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.repository import Repository
from models.user import User
from os import environ
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from hashlib import md5
app = Flask(__name__)
app.secret_key = '2K24_06_shared_key'
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
@app.route('/index', strict_slashes=False)
def index():
    """ Returns the landing page. """
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def create_user():
    """ Creates a new user or return the signup page. """
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        if not request.form:
            return render_template('signup.html')
        else:
            data = request.form.to_dict()
            new = User(**data)
            new.save()
            return render_template('login.html',
                                   msg = 'Sign up Successful, Now Login')

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ User Login """
    if request.method == 'POST':
        users = storage.all(User).values()
        email = request.form['email']
        password = request.form['password']
        password = md5(password.encode()).hexdigest()
        for user in users:
            if user.email == email and user.password == password:
                login_user('User' + user.id)
                return redirect(url_for('repos'))
            else:
                return render_template('login.html',
                                       msg='Wrong email or password')
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/logout', strict_slashes=False)
@login_required
def logout():
    """ Log's a user out """
    logout_user()
    return render_template('login.html', msg='Logged Out')


@app.route('/repos', methods=['GET'], strict_slashes=False)
@app.route('/repos/<repo_id>', methods=['GET'], strict_slashes=False)
@login_required
def repos():
    """ Returns a list of saved repositories """
    repos = storage.all(Repository).values()
    repos = sorted(repos, key=lambda k: k.name)
    data = []

    return render_template('repos.html', data=data)


@app.route('/repos/<repo_id>', methods=['PUT', 'POST', 'DELETE'], strict_slashes=False)
@login_required
def repo(repo_id=None):
    """ Handles repository creaton, update, and delete """
    if request.methods == 'POST':
        pass


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
