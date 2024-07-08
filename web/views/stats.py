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
    total_c = total_issues = 0
    t_commits = 0
    pull = 0
    name = []

    if contributors and len(contributors) != 0:
        total_c = len(contributors)
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
        top_c = {"names": name, "commits": c}
        del contributors
    else:
        top_c = {"names": [], "commits": []}

    # All commits from the first commit date to the curent date
    daily_commits = defaultdict(int)
    weekly_commits = defaultdict(int)
    url = "https://api.github.com/repos/{}/{}/commits?per_page=100"\
          .format(repo.owner, repo.repo_name)
    commits = get_stats(url, headers)

    if commits:
        for commit in commits:
            c_date = datetime.strptime(commit['commit']['committer']['date'],
                    "%Y-%m-%dT%H:%M:%SZ").date()
            daily_commits[c_date] += 1
            weekly_commits[week_start(c_date)] += 1
            t_commits += 1

        # Add missing days
        first_date = min(daily_commits.keys())
        last_date = datetime.now().date()
        all_dates = list_of_days(first_date, last_date)
        for date in all_dates:
            if date not in daily_commits:
                daily_commits[date] = 0
            if week_start(date) not in weekly_commits:
                weekly_commits[week_start(date)] = 0

        # Sort and format for jsonification
        daily_commits = dict(sorted(daily_commits.items()))
        d = [key.strftime("%Y-%m-%d") for key in daily_commits.keys()]
        c = [count for count in daily_commits.values()]
        d_commits = {"dates": d, "commits": c}

        weekly_commits = dict(sorted(weekly_commits.items()))
        d = [key.strftime("%Y-%m-%d") for key in weekly_commits.keys()]
        c = [count for count in weekly_commits.values()]
        w_commits = {"dates": d, "commits": c}

        # Commits for the last 7 days
        week_list = list(daily_commits.items())[-7:]
        week_commits = dict(week_list)
        d = [key.strftime("%m-%d") for key in week_commits.keys()]
        c = [count for count in week_commits.values()]
        week_c = {"dates": d, "commits": c}

        # Commits for the last 8 weeks
        if len(weekly_commits) > 8:
            weeks_list = list(weekly_commits.items())[-8:]
            weeks_commits = dict(weeks_list)
        else:
            weeks_commits = weekly_commits

        d = [key.strftime("%Y-%m-%d") for key in weeks_commits.keys()]
        c = [count for count in weeks_commits.values()]
        w_commits = {"dates": d, "commits": c}

        # Commits for the last 52 weeks
        if len(weekly_commits) > 52:
            weeks_list = list(weekly_commits.items())[-52:]
            weeks_commits = dict(weeks_list)
        else:
            weeks_commits = weekly_commits

        d = [key.strftime("%Y-%m-%d") for key in weeks_commits.keys()]
        c = [count for count in weeks_commits.values()]
        w52_commits = {"dates": d, "commits": c}
    else:
        d_commits = {"dates": [], "commits": []}
        week_c = {"dates": [], "commits": []}
        w_commits = {"dates": [], "commits": []}
        w52_commits = {"dates": [], "commits": []}

    # Returns all issues
    url = "https://api.github.com/repos/{}/{}/issues?state=all&\
           per_page=100".format(repo.owner, repo.repo_name)
    issues = get_stats(url, headers)

    daily_opened_issues = defaultdict(int)
    weekly_opened_issues = defaultdict(int)
    daily_closed_issues = defaultdict(int)
    weekly_closed_issues = defaultdict(int)

    if issues:
        for issue in issues:
            total_issues += 1
            created_date = datetime.strptime(issue['created_at'],
                                         "%Y-%m-%dT%H:%M:%SZ").date()
            daily_opened_issues[created_date] += 1
            weekly_opened_issues[week_start(created_date)] += 1

            if issue.get('closed_at'):
                closed_date = datetime.strptime(issue['closed_at'],
                                                "%Y-%m-%dT%H:%M:%SZ").date()
                daily_closed_issues[closed_date] += 1
                weekly_closed_issues[week_start(closed_date)] += 1

        # Add missing day and weeks
        first_date = min(daily_opened_issues.keys())
        last_date = datetime.now().date()
        all_days = list_of_days(first_date, last_date)
        for day in all_days:
            if day not in daily_opened_issues:
                daily_opened_issues[day] = 0
            if week_start(day) not in weekly_opened_issues:
                weekly_opened_issues[week_start(day)] = 0

            if day not in daily_closed_issues:
                daily_closed_issues[day] = 0
            if week_start(day) not in weekly_closed_issues:
                weekly_closed_issues[week_start(day)] = 0

        # Sort and format for Jsonification
        daily_opened_issues = dict((sorted(daily_opened_issues.items())))
        weekly_opened_issues = dict((sorted(weekly_opened_issues.items())))
        daily_closed_issues = dict((sorted(daily_closed_issues.items())))
        weekly_closed_issues = dict((sorted(weekly_closed_issues.items())))
        d = [key.strftime("%Y-%m-%d") for key in daily_opened_issues.keys()]
        c = [count for count in daily_opened_issues.values()]
        daily_issues_all = {"dates": d, "open": c}
        c = [count for count in daily_closed_issues.values()]
        daily_issues_all['closed'] = c

        d = [key.strftime("%Y-%m-%d") for key in weekly_opened_issues.keys()]
        c = [count for count in weekly_opened_issues.values()]
        weekly_issues_all = {"dates": d, "open": c}
        d = [key.strftime("%Y-%m-%d") for key in weekly_closed_issues.keys()]
        c = [count for count in weekly_closed_issues.values()]
        weekly_issues_all['closed'] = c

        # Issues for the last 7 days
        if len(daily_opened_issues) > 7:
            week_list = list(daily_opened_issues.items())[-7:]
            week_open_issues = dict(week_list)
            week_list = list(daily_closed_issues.items())[-7:]
            week_close_issues = dict(week_list)
        else:
            week_open_issues = daily_opened_issues
            week_close_issues = daily_closed_issues

        # Open and closed issues for the last 7 days
        d = [key.strftime("%m-%d") for key in week_open_issues.keys()]
        c = [count for count in week_open_issues.values()]
        d_issues = {"dates": d, "open": c}
        c = [count for count in week_commits.values()]
        d_issues['closed'] = c

        # Issues for the last 8 weeks
        if len(weekly_opened_issues) > 8:
            weekly_list = list(weekly_opened_issues.items())[-8:]
            weekly_open_issues = dict(weekly_list)
            weekly_list = list(weekly_closed_issues.items())[-8:]
            weekly_close_issues = dict(weekly_list)
        else:
            weekly_open_issues = weekly_opened_issues
            weekly_close_issues = weekly_closed_issues

        # Open and closed issues for the last 8 weeks
        d = [key.strftime("%m-%d") for key in weekly_open_issues.keys()]
        c = [count for count in weekly_open_issues.values()]
        w_issues = {"dates": d, "open": c}
        c = [count for count in weekly_closed_issues.values()]
        w_issues['closed'] = c

        # Issues for the last 52 weeks
        if len(weekly_opened_issues) > 52:
            weekly_list = list(weekly_opened_issues.items())[-52:]
            weekly_open_issues = dict(weekly_list)
            weekly_list = list(weekly_closed_issues.items())[-52:]
            weekly_close_issues = dict(weekly_list)
        else:
            weekly_open_issues = weekly_opened_issues
            weekly_close_issues = weekly_closed_issues

        # Open and closed issues for the last 52 weeks
        d = [key.strftime("%m-%d") for key in weekly_open_issues.keys()]
        c = [count for count in weekly_open_issues.values()]
        w52_issues = {"dates": d, "open": c}
        c = [count for count in weekly_closed_issues.values()]
        w52_issues['closed'] = c
    else:
        d_issues = {"dates": [], "open": [], "closed": []}
        w_issues = {"dates": [], "open": [], "closed": []}
        w52_issues = {"dates": [], "open": [], "closed": []}

    data = {
        "commits": t_commits,
        "pull": pull,
        "total_c": total_c,
        "total_issues": total_issues,
        "names": name
    }

    return render_template('stats.html',
                           data=data,
                           all_time=json.dumps(d_commits),
                           top_c=json.dumps(top_c),
                           week=json.dumps(week_c),
                           w_commits=json.dumps(w_commits),
                           w52_commits=json.dumps(w52_commits),
                           d_issues=json.dumps(d_issues),
                           w_issues=json.dumps(w_issues),
                           w52_issues=json.dumps(w52_issues))


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

def week_start(date):
    """ Take a date and return the date of the first day of the
        week for the given date """
    return date - timedelta(days=date.weekday())

def list_of_days(first_date, last_date):
    """ Returns a list of days. """
    return [first_date + timedelta(days=i) for i in\
            range((last_date - first_date).days + 1)]
