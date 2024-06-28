#!/usr/bin/python3
""" Handles the repo and stats page requests. """
from models import storage
from models.repository import Repository
from models.user import User
from flask import abort, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from web.views import app_views


@app_views.route('/repos', methods=['GET'],
                 strict_slashes=False)
@login_required
def repos():
    """ Retrieves all repositories related to a user. """
    repos = [repo for repo in current_user.repos]
    return render_template('repos.html', repos=repos)

@app_views.route('/add_repo', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def addRepo():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        if not request.form:
            return render_template('add.html')
        if not request.form['name'] or request.form['name'] == "":
            return render_template('add.html',
                                   data=request.form,
                                   msg='Project name missing')
        if not request.form['owner'] or request.form['owner'] == "":
            return render_template('add.html',
                                   data=request.form,
                                   msg='Project owner name missing')
        if not request.form['link'] or request.form['link'] == "":
            return render_template('add.html',
                                   data=request.form,
                                   msg='Repository link missing')
        if not request.form['privacy'] or request.form['privacy'] == "":
            return render_template('add.html',
                                   data=request.form,
                                   msg='Privacy option missing')
        if request.form['privacy'] == "private" and request.form['pat'] == "":
            return render_template('add.html',
                                   data=request.form,
                                   msg='Personal Access Tokens are necessary for \
                                        private repository')
        data = request.form.to_dict()
        data['user_id'] = current_user.id
        newRepo = Repository()
        for key, value in data.items():
            setattr(newRepo, key, value)
        newRepo.save()
        return redirect(url_for('app_views.repos'))


@app_views.route('/stats/<repo_id>', methods=['GET'], strict_slashes=False)
@login_required
def stats(repo_id):
    """ Handles all actions that an be performed on a single repo """
    repo = storage.get(Repository, repo_id)
    if current_user.id != repo.user_id:
        abort(404)
    return render_template('stats.html', repo=repo)


@app_views.route('/edit_repo/<repo_id>', methods=['GET', 'POST'],
           strict_slashes=False)
@login_required
def editRepo(repo_id):
    """ Edits a repository """
    repos = current_user.repos
    if not repos:
        return redirect(url_for('app_views.repos'))
    for rep in repos:
        if rep.id == repo_id:
            repo = rep
    if not repo:
        return redirect(url_for('app_views.repos'))
    if request.method == 'GET':
        return render_template('edit.html', data=repo)
    elif request.method == 'POST':
         pass


@app_views.route('/repo/<repo_id>/delete', methods=['GET'],
           strict_slashes=False)
@login_required
def deleteRepo(repo_id):
    """ Deletes a repository """
    repo = storage.get(Repository, repo_id)
    if not repo:
        abort(404)
    if current_user.id != repo.user_id:
        abort(404)
    storage.delete(repo)
    storage.save()

    return redirect(url_for('app_views.repos'))
