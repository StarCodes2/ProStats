#!/usr/bin/python3
"""
initialize the models package
"""
from os import getenv


storage_t = getenv("TYPE_STORAGE")
from models.engine.db_storage import DBStorage
storage = DBStorage()
storage.reload()
