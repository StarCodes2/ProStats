#!/usr/bin/python3
""" Handles the repo and stats page requests. """
from models import storage
from models.repository import Repository
from models.user import User
from flask import abort, render_template, request
from flask_login import current_user, login_required
from web.views import app_views


@app_views.route('/repos/<user_id>', methods=['GET', 'POST'],
                 strict_slashes=False)
@login_required
def repos(user_id=None):
    """ Retrieves all repositories or creates a new one. """
    if request.method == 'GET' and user_id is not None:
        user = storage.get(User, user_id)
        if not user or user_id != current_user.id:
            abort(404)

        repos = [repo for repo in user.repos]
        return render_template('repos.html', repos=repos)
    elif request.method == 'POST':
        if not request.form['name']:
            abort(400, 'Project name missing')
        if not request.form['owner']:
            about(400, 'Project owner name missing')
        if not request.form['link']:
            abort(400, 'Repository lin missing')
        if not request.form['privacy']:
            abort(400, 'Privacy option missing')
        if request.form['privacy'] == 'private' and not request.form['pat']:
            abort(400, 'Personal Access Tokens are necessary for \
                  private repository')
        user = storage.get(User, user_id)
        if not user or user_id != current_user.id:
            abort(404)

        data = request.form
        data['user_id'] = user_id
        newRepo = Repository(**data)
        newRepo.save()
        return render_template('repo.html', repos=user.repos.values())


@app_views.route('/stats/<repo_id>', methods=['GET'], strict_slashes=False)
@login_required
def stats(repo_id):
    """ Handles all actions that an be performed on a single repo """
    repo = storage.get(Repository, repo_id)
    if current_user.id != repo.user_id:
        abort(404)
    return render_template('stats.html', repo=repo)


@app_views.route('/repo/<repo_id>/edit', methods=['GET', 'POST'],
           strict_slashes=False)
@login_required
def editRepo(repo_id):
    """ Edits a repository """
    repo = storage.get(Repository, repo_id)
    if not repo:
        abort(404)
    if current_user.id != repo.user_id:
        abort(404)
    if request.method == 'GET':
        return render_template('edit.html', repo=repo)
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

    return render_template('repos.html', repos=repos)
