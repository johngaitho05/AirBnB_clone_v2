#!/usr/bin/python3
"""Defines the User class."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel
from . import storage_type

if storage_type == 'db':
    class User(BaseModel, Base):
        """
        Represents a User ORM
        """

        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete-orphan")
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
        first_name = ""
        last_name = ""
        password = ""
