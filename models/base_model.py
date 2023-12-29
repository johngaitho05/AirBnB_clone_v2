#!/usr/bin/python3
"""
This is an abstraction class to be inherited by other classes of the project
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

from models import storage_type

Base = declarative_base()


class BaseModel:
    """
    Defines all common attributes/methods for other classes
    """

    defaults = {}

    if storage_type == 'db':
        id = Column(String(60), primary_key=True, nullable=False, unique=True)
        created_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow(),
                            nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialization"""
        for k, v in self.__class__.defaults.items():
            if k not in kwargs:
                kwargs.update({k: v})
        if kwargs:
            forbidden_keys = ['__class__']
            datetime_keys = ['created_at', 'updated_at']
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid.uuid4())
            now = kwargs['created_at'] = datetime.now().isoformat()
            if 'created_at' not in kwargs:
                kwargs['created_at'] = now
            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = now
            if '_sa_instance_state' in kwargs:
                del kwargs['_sa_instance_state']
            for k, v in kwargs.items():
                if k in forbidden_keys:
                    continue
                if k in datetime_keys:
                    # convert to datetime object
                    v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            now = datetime.now()
            self.created_at = now
            self.updated_at = now

    def __str__(self):
        """Returns the string representation of an instance"""
        # forbidden = ['_sa_instance_state']
        # d = {k: v for k, v in self.__dict__.items() if k not in forbidden}
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """updates the public instance attribute updated_
        at with the current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of an object"""
        res = self.__dict__.copy()
        res['__class__'] = self.__class__.__name__
        res['created_at'] = self.created_at.isoformat()
        res['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in res:
            del res['_sa_instance_state']
        return res

    def delete(self):
        """Deletes an instance from storage"""
        from models import storage
        storage.delete(self)
