#!/usr/bin/python3
""" Handles the repo and stats page requests. """
from collections import defaultdict
from datetime import datetime, timedelta
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
    d_commits = {}
    week_c = {}
    total_c = 0
    t_commits = 0
    pull = 0
    if contributors and len(contributors) != 0:
        total_c = len(contributors)
        name = []
        c = []
        count = 0
        for contri in contributors:
            if count <= 5:
                name.append(contri['login'])
                c.append(contri['contributions'])
                count += 1
            else:
                name[-1] = "others"
                c[-1] += contri['contributions']
        top_c['names'] = name
        top_c['commits'] = c
        del contributors

    # All commits from the first commit date to the curent date
    daily_commits = defaultdict(int)
    url = "https://api.github.com/repos/{}/{}/commits?per_page=100"\
          .format(repo.owner, repo.repo_name)
    commits = get_stats(url, headers)

    for commit in commits:
        c_date = datetime.strptime(commit['commit']['committer']['date'],
                "%Y-%m-%dT%H:%M:%SZ").date()
        daily_commits[c_date] += 1
        t_commits += 1

    if commits:
        first_date = min(daily_commits.keys())
        last_date = datetime.now().date()
        all_dates = [first_date + timedelta(days=i) for i in\
                     range((last_date - first_date).days + 1)]
        for date in all_dates:
            if date not in daily_commits:
                daily_commits[date] = 0
        daily_commits = dict((sorted(daily_commits.items())))
        d = [key.strftime("%Y-%m-%d") for key in daily_commits.keys()]
        c = [count for count in daily_commits.values()]
        d_commits['days'] = d
        d_commits['commits'] = c

        # Commits for the last 7 days
        week_list = list(daily_commits.items())[-7:]
        week_commits = dict(week_list)
        d = [key.strftime("%m-%d") for key in week_commits.keys()]
        c = [count for count in week_commits.values()]
        week_c['days'] = d
        week_c['commits'] = c

    # Returns all issues
    url = "https://api.github.com/repos/{}/{}/issues?state=all\
           &per_page=100".format(repo.owner, repo.repo_name)

    # Returns commits for the last 52 weeks.
    url = "https://api.github.com/repos/{}/{}/stats/participation"\
          .format(repo.owner, repo.repo_name)

    data = {
        "commits": t_commits,
        "pull": pull,
        "total_c": total_c,
        "names": name
    }

    return render_template('stats.html',
                           data=data,
                           all_time=json.dumps(d_commits),
                           top_c=json.dumps(top_c),
                           week=json.dumps(week_c))


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
