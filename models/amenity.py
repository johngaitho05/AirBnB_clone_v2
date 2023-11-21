#!/usr/bin/python3
"""
Defines the Amenity class.
"""

from sqlalchemy import Column, String

from models.base_model import BaseModel
from models.engine.db_storage import Base
from . import storage_type

if storage_type == 'db':

    class Amenity(BaseModel, Base):
        """
        Represent an amenity.
        """
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)

else:
    class Amenity(BaseModel):
        """
        Represent an amenity.
        """
        name = ""

Amenity.defaults = {
    'name': ""
}
