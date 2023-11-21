#!/usr/bin/python3
"""
Defines the City class.
"""
from sqlalchemy import Column, String, ForeignKey

from models.base_model import BaseModel
from models.engine.db_storage import Base
from . import storage_type


if storage_type == 'db':
    class City(BaseModel, Base):
        """
         City ORM
        """
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
else:
    class City(BaseModel):
        """
        A blueprint for a City object
        """

        state_id = ""
        name = ""

