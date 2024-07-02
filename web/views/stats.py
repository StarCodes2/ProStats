#!/usr/bin/python3
""" Handles the repo and stats page requests. """
from models import storage
from models.repository import Repository
from models.user import User
from flask import abort, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from web.views import app_views
import requests
import json


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

    headers = {'Authorization': "token {}".format(repo.pat)}
    url = "https://api.github.com/repos/{}/{}/contributors?state=all\
           &per_page=100".format(repo.owner, repo.repo_name)
    contributors = get_stats(url, headers)
    top_c = {}
    total_c = 0
    commits = 0
    pull = 0
    if contributors and len(contributors) != 0:
        total_c = len(contributors)
        name = []
        c = []
        count = 0
        for contri in contributors:
            commits += contri['contributions']
            if count <= 5:
                name.append(contri['login'])
                c.append(contri['contributions'])
                count += 1
            else:
                name[-1] = "others"
                c[-1] += contri['contributions']
        top_c['names'] = name
        top_c['commits'] = c

    url = "https://api.github.com/repos/{}/{}/contributors?state=all\
           &per_page=100".format(repo.owner, repo.repo_name)

    """Returns commits for the last 52 weeks."""
    url = "https://api.github.com/repos/{}/{}/stats/participation"\
          .format(repo.owner, repo.repo_name)

    data = {
        "commits": commits,
        "pull": pull,
        "total_c": total_c,
        "names": name
    }

    return render_template('stats.html',
                           data=data,
                           top_c=json.dumps(top_c))


def get_stats(url, headers):
    """ Returns a list containing the response from the api call """
    try:
        result = []
        while url:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result.extend(response.json())
                if 'next' in response.links:
                    url = response.links['next']['url']
                else:
                    url = None
        return result
    except:
        return None
