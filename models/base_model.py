#!/usr/bin/python3
'''This module contains the definition of the BaseModel class which is the
base for the classes of data in the AirBnB clone app
'''
import uuid
from datetime import datetime


class BaseModel:
    '''The base class for the classes of data in the AirBnB clone app
    '''

    def __init__(self, *args, **kwargs):
        '''The initializer method for BaseModel instances
        Rereates objects if kwargs is passed in and
        creates new ones elsewise'''
        if kwargs:
            for key in kwargs:
                if key == "__class__":
                    continue
                elif key in ("created_at", "updated_at"):
                    setattr(self, key, datetime.fromisoformat(kwargs[key]))
                else:
                    setattr(self, key, kwargs[key])
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

            storage = __import__('', globals(), fromlist=["storage"],
                                 level=1).storage
            storage.new(self)

    def __str__(self):
        '''Returns the string represntation of the class instance'''
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        '''Saves the current object to the active storage engine and
         updates the instance variable <updated_to> with the current time
        '''
        self.updated_at = datetime.now()

        storage = __import__('', globals(), fromlist=["storage"],
                             level=1).storage
        storage.save()

    def to_dict(self):
        '''Returns dictionary representaion of the class instance:
        - Contains all keys/values of __dict__ of the instance
        - The values of the keys <created_at> and <updated_at> are converted
          to string object in ISO format
        - A key <__class__> is added to the dictionary with the class name of
          the object as its key
        '''
        out = self.__dict__.copy()
        out["created_at"] = self.created_at.isoformat()
        out["updated_at"] = self.updated_at.isoformat()
        out["__class__"] = self.__class__.__name__
        return out
