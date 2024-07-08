#!/usr/bin/python3
""" Blueprint for ProStat """
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from views.index import *
from views.repository import *
from views.stats import *
