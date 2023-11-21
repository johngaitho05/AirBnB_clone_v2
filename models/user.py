#!/usr/bin/python3
"""Defines the User class."""
from sqlalchemy import Column, String

from models.base_model import BaseModel
from .engine.db_storage import Base


class User(BaseModel, Base):
    """
    User ORM
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
