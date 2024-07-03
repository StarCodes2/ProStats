#!/usr/bin/python3
""" Starts a Flash Web Application """
import re
from models import storage
from models.repository import Repository
from models.user import User
from os import environ
from flask import Flask, render_template, request, redirect, make_response, url_for
from flask_login import login_user, login_required, logout_user, current_user
from hashlib import md5
from web.views import app_views


@app_views.route('/', strict_slashes=False)
@app_views.route('/index', strict_slashes=False)
@login_required
def index():
    """ Returns the landing page. """
    return render_template('index.html')

@app_views.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def create_user():
    """ Creates a new user or return the signup page. """
    if current_user.is_authenticated:
        return redirect(url_for('app_views.repos'))

    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        if not request.form:
            return render_template('signup.html')
        else:
            data = request.form.to_dict()
            regUser = storage.getByValue(User, 'email', data['email'])
            if regUser:
                return render_template('signup.html',
                                       data=data,
                                       msg="Email already linked to an account!")

            if data['email'] == "" or data['first_name'] == "" \
            or data['last_name'] =="" or data['password'] == "":
                return render_template('signup.html',
                                       data=data,
                                       msg="All fields are required")

            if not is_valid_email(data['email']):
                return render_template('signup.html',
                                       data=data,
                                       msg="Invalid email address")

            if not is_valid_password(data['password']):
                msg = "Password must be at least 8 characters long and \
                        contain both letters and numbers"
                return render_template('signup.html',
                                       data=data,
                                       msg=msg)

            if data['password'] != data['re-enter']:
                return render_template('signup.html',
                                       data=data,
                                       msg="Passwords do not match!")

            new = User()
            for key, value in data.items():
                if key != "password":
                    setattr(new, key, value)
                else:
                    new.setAttrMd5(key, value)
            new.save()
            return render_template('login.html',
                                   msg = 'Sign up Successful, Now Login')

@app_views.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ User Login """
    if current_user.is_authenticated:
        return redirect(url_for('app_views.repos'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == "" or password == "":
            return render_template('login.html', msg='Enter your email and password')
        password = md5(password.encode()).hexdigest()

        user = storage.getByValue(User, 'email', email)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('app_views.repos'))
        return render_template('login.html',
                               msg='Wrong email or password')
    elif request.method == 'GET':
        return render_template('login.html')


@app_views.route('/logout', strict_slashes=False)
@login_required
def logout():
    """ Log's a user out """
    logout_user()
    return redirect(url_for('app_views.login'))


def is_valid_email(email):
    """ Checks if email matches an actual email format. """
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$')
    return email_pattern.match(email) is not None


def is_valid_password(password):
    """ Checks if password meets requirement """
    pass_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
    return pass_pattern.match(password) is not None

