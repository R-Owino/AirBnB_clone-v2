#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
import models
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == 'db':
    Base = declarative_base()
else:
    Base = object


time_fmt = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """A base class for all hbnb models
    Attributes:

        id(SQLalchemy String): The BaseModel id
        created_at(SQLalchemy date time): The date time at creation
        updated_at(SQLalchemy date time): The date time when updated
    """
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        id = Column(String(60),
                    primary_key=True,
                    nullable=False)
        created_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at, time_fmt)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at, time_fmt)

    def __str__(self):
        """Returns a string representation of the instance"""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        my_dict.pop('_sa_instance_state', None)
        return my_dict

    def delete(self):
        """Delete current instance from storage by calling its delete method"""
        models.storage.delete(self)
