#!/usr/bin/python3
"""Defines the States."""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_type
from models.base_model import Base, BaseModel
from .city import City

if storage_type == 'db':
    class State(BaseModel, Base):
        """
        State ORM
        """
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")

else:
    class State(BaseModel):
        """Attributes:
        name (str): The name of the state.
        """

        name = ""

        @property
        def cities(self):
            from models import storage
            all_cities = list(storage.all(City).values())
            return list(filter((lambda c: c.state_id == self.id), all_cities))
