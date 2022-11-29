#!/usr/bin/python3
"""This module contains the difinition of the BaseModel class"""

from datetime import datetime
from uuid import uuid4

import models
# storage = ''


class BaseModel:
    """The base model for all the objects of the app"""

    # from . import storage
    def __init__(self, *args, **kwargs):
        """Creates an object of the class"""

        if not len(kwargs):
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

            from . import storage
            self.__class__.storage = storage
            storage.new(self)
            return

        for key, val in kwargs.items():
            if key == "__class__":
                continue
            elif key == "created_at":
                self.created_at = datetime.fromisoformat(val)
            elif key == "updated_at":
                self.updated_at = datetime.fromisoformat(val)
            else:
                setattr(self, key, val)

    def __str__(self):
        """Returns the string representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates self.updated_at with the current datetime"""
        self.updated_at = datetime.now()
        self.storage.new(self)
        self.storage.save()
        pass

    def to_dict(self):
        """Returns a dictionary representation of the object"""
        dictionary = dict(self.__dict__)
        dictionary["__class__"] = self.__class__.__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary
    pass
