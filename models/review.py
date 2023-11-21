#!/usr/bin/python3
"""Defines the Review class."""
from sqlalchemy import Column, String, ForeignKey

from models.base_model import BaseModel
from models.engine.db_storage import Base
from . import storage_type

if storage_type == 'db':
    class Review(BaseModel, Base):
        """
        Review ORM
        """
        defaults = {'place_id': "", 'user_id': "", 'text': ""}

        __tablename__ = 'reviews'

        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
else:
    class Review(BaseModel):
        """Represent a review.

        Public attributes:
            place_id (str): The Place id.
            user_id (str): The User id.
            text (str): The text of the review.
        """

        defaults = {'place_id': "", 'user_id': "", 'text': ""}
