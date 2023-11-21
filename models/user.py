#!/usr/bin/python3
"""Defines the User class."""
from sqlalchemy import Column, String

from models.base_model import BaseModel
from models.engine.db_storage import Base
from . import storage_type

if storage_type == 'db':
    class User(BaseModel, Base):
        """
        User ORM
        """
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)

else:
    class User(BaseModel):
        """Represent a User.

        Public class attributes:
            email (str): The email of the user.
            password (str): The password of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
        """

        email = ""
        password = ""
        first_name = ""
        last_name = ""
