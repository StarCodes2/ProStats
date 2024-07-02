#!/usr/bin/python3
""" Blueprint for ProStat """
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from web.views.index import *
from web.views.repository import *
from web.views.stats import *
