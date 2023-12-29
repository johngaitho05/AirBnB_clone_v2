#!/usr/bin/python3
"""Defines the DBStorage class."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()


class DBStorage:
    """
    Represent an abstracted storage engine using MySQL database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializer"""
        username = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(username, password, host,
                                             database),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return all records of the given class"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classes = [State, City, User, Place, Review, Amenity]
        if cls:
            res = self.__session.query(cls).all()
        else:
            res = []
            for klas in classes:
                res += self.__session.query(klas).all()
        return {"{}.{}".format(obj.__class__.__name__, obj.id): obj
                for obj in res}

    def new(self, obj):
        """Create a new record"""
        self.__session.add(obj)

    def save(self):
        """save a record"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes a record from session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads the data"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes a session"""
        self.__session.close()
