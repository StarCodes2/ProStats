#!/usr/bin/python3
""" Handles the repo and stats page requests. """
from models import storage
from models.repository import Repository
from models.user import User
from flask import abort, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from web.views import app_views
import requests


@app_views.route('/repos', methods=['GET'],
                 strict_slashes=False)
@login_required
def repos():
    """ Retrieves all repositories related to a user. """
    repos = {}
    if not current_user.repos:
        repos = None
    for repo in current_user.repos:
        repos[repo.id] = repo.to_dict()

        url = "https://api.github.com/repos/{}/{}/commits"\
              .format(repo.owner,
                      repo.repo_name)
        headers = {'Authorization': "token {}".format(repo.pat)}
        total_commits = count_res(url, headers)
        url = "https://api.github.com/repos/{}/{}/pulls?state=all"\
              .format(repo.owner,
                      repo.repo_name)
        total_pull = count_res(url, headers)

        if not total_commits:
            total_commits = 0
        if not total_pull:
            total_pull = 0
        repos[repo.id]['total_commits'] = total_commits
        repos[repo.id]['total_pull'] = total_pull

    return render_template('repos.html', repos=repos)


def count_res(url, headers):
    """ Count the total amount of data entry in all the
    pages of an api endpoint """
    try:
        total = 0
        while url:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                total += len(data)
                url = response.links.get('next', {}).get('url')
            else:
                return None
        return total
    except:
        return None


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
        if not request.form['repo_name'] or request.form['repo_name'] == "":
            return render_template('add.html',
                                   data=request.form,
                                   msg='Repository name is missing')
        if not request.form['privacy'] or request.form['privacy'] == "":
            return render_template('add.html',
                                   data=request.form,
                                   msg='Privacy option not selected')
        if not request.form['pat'] or request.form['pat'] == "":
            return render_template('add.html',
                                   data=request.form,
                                   msg='Personal Access Token is missing')
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
    repos = current_user.repos
    for obj in repos:
        if obj.id == repo_id:
            repo = obj
    if not repo:
        return redirect('app_views.repos')
    url = "".format()

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
        if not request.form:
            return redirect(url_for('app_views.addRepo'))
        if not request.form['name'] or request.form['name'] == "":
            return render_template('edit.html',
                                   data=request.form,
                                   msg='Project name missing')
        if not request.form['owner'] or request.form['owner'] == "":
            return render_template('edit.html',
                                   data=request.form,
                                   msg='Project owner name missing')
        if not request.form['repo_name'] or request.form['repo_name'] == "":
            return render_template('edit.html',
                                   data=request.form,
                                   msg='Repository name is missing')
        if not request.form['privacy'] or request.form['privacy'] == "":
            return render_template('edit.html',
                                   data=request.form,
                                   msg='Privacy option not selected')
        if not request.form['pat'] or request.form['pat'] == "":
            return render_template('edit.html',
                                   data=request.form,
                                   msg='Personal Access Token is missing')
        data = request.form.to_dict()
        for key, value in data.items():
            setattr(repo, key, value)
        repo.save()
        return redirect(url_for('app_views.repos'))


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
