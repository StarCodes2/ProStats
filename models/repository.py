#!/usr/bin/python
""" holds class Repository"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Boolean, ForeignKey


class Repository(BaseModel, Base):
    """Representation of Repository """
    if models.storage_t == 'db':
        __tablename__ = 'repositories'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        project_name = Column(String(128), nullable=False)
        repo_link = Column(String(1024), nullable=False)
        public = Column(Boolean, nullable=False, default=True)
        pat = Column(String(60), nullable=True)
    else:
        user_id = ""
        project_name = ""
        owner = ""
        repo_link = 0
        public = False
        pat = ""

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
