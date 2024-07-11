#!/usr/bin/python3
""" holds class User"""

from flask_login import UserMixin
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, UserMixin, Base):
    """Representation of a user """
    __tablename__ = 'users'
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    repos = relationship("Repository", backref="user")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def setAttrMd5(self, name, value):
        """encrypt attribute with md5 encryption"""
        value = md5(value.encode()).hexdigest()
        setattr(self, name, value)
