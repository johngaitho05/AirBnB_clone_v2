#!/usr/bin/python3
"""Defines the Place class."""
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel
from models import storage_type
from .amenity import Amenity
from .review import Review

if storage_type == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 nullable=False)
                          )

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
        reviews = relationship("Review", backref="place",
                               cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False)

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

        @property
        def reviews(self):
            from models import storage
            all_reviews = list(storage.all(Review).values())
            return list(filter((lambda c: c.place_id == self.id), all_reviews))

        @property
        def amenities(self):
            from models import storage
            all_amenities = list(storage.all(Amenity).values())
            return list(filter((lambda a: a.id in self.amenity_ids),
                               all_amenities))

        @amenities.setter
        def amenities(self, value):
            if isinstance(value, Amenity):
                self.amenity_ids.append(Amenity.id)
