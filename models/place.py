#!/usr/bin/python3
"""Defines the Place class."""
from sqlalchemy import Column, String, ForeignKey, Integer, Float

from models.base_model import BaseModel
from models.engine.db_storage import Base
from . import storage_type

if storage_type == 'db':
    class Place(BaseModel, Base):
        """
        Place ORM
        """
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

else:
    class Place(BaseModel):
        """Represents a place.

        Public attributes:
            city_id (str): The City id.
            user_id (str): The User id.
            name (str): The name of the place.
            description (str): The description of the place.
            number_rooms (int): The number of rooms of the place.
            number_bathrooms (int): The number of bathrooms of the place.
            max_guest (int): The maximum number of guests of the place.
            price_by_night (int): The price by night of the place.
            latitude (float): The latitude of the place.
            longitude (float): The longitude of the place.
            amenity_ids (list): A list of Amenity ids.
        """

        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []



