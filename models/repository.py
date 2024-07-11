#!/usr/bin/python
""" holds class Repository"""
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey


class Repository(BaseModel, Base):
    """Representation of Repository """
    __tablename__ = 'repositories'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    owner = Column(String(128), nullable=False)
    repo_name = Column(String(1024), nullable=False)
    privacy = Column(String(8), nullable=False, default="public")
    pat = Column(String(60), nullable=True)

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
