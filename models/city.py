#!/usr/bin/python3
"""
Defines the City class.
"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

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
        state_id = Column(String(60), ForeignKey('states.id'),
                          nullable=False, )
        places = relationship("Place", backref="cities",
                              cascade="all, delete-orphan")
else:
    class City(BaseModel):
        """
        A blueprint for a City object
        """

        places = ""


City.defaults = {
        'state_id': "",
        'name': "",
    }
