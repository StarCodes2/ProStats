#!/usr/bin/python
""" holds class Repository"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Repository(BaseModel, Base):
    """Representation of Repository """
    if models.storage_t == 'db':
        __tablename__ = 'repositories'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        owner = Column(String(128), nullable=False)
        link = Column(String(1024), nullable=False)
        privacy = Column(String(8), nullable=False, default="public")
        pat = Column(String(60), nullable=True)
    else:
        user_id = ""
        name = ""
        owner = ""
        link = 0
        privacy = False
        pat = ""

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
