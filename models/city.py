#!/usr/bin/python3
"""
Defines the City class.
"""
from sqlalchemy import Column, String, ForeignKey

from models.base_model import BaseModel
from models.engine.db_storage import Base


class City(BaseModel, Base):
    """
     City ORM
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

