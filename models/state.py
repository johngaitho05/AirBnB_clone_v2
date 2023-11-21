#!/usr/bin/python3
"""Defines the States."""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from . import storage, storage_type

from models.engine.db_storage import Base
from models.base_model import BaseModel
from .city import City


class State(BaseModel, Base):
    """
    State ORM
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    if storage_type == 'db':
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:

        @property
        def cities(self):
            all_cities = list(storage.all(City).values())
            return list(filter((lambda c: c.state_id == self.id), all_cities))
