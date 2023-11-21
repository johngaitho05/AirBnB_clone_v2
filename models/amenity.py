#!/usr/bin/python3
"""
Defines the Amenity class.
"""
from models.base_model import BaseModel

from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship

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
