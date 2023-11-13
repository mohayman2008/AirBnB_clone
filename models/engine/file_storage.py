#!/usr/bin/python3
'''This module contains the definition of the FileStorage class which is the
file storage data engine in the AirBnB clone app
'''
import json
import os

from ..base_model import BaseModel
from ..user import User
from ..state import State
from ..city import City
from ..amenity import Amenity
from ..place import Place
from ..review import Review


class FileStorage:
    '''The file storage data engine in the AirBnB clone app
    Class variables:
        __file_path: path to the JSON file to store serialized data
        __objects: dictionary to contain all objects with keys
                   in the form '<class name>.id'
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self):
        '''Returns a copy of <__objects> dictionary'''
        return self.__objects

    def new(self, obj):
        '''Adds 'obj' to '__objects' dictionary with the key
        '<obj class name>.id'
        '''
        __class__.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
        self.save()

    def save(self):
        '''Serializes '__objects' dictionary to JSON and stores it to
        the JSON file located at '__file_path'
        '''
        objects = {}
        for key, obj in self.__objects.items():
            objects[key] = obj.to_dict()

        with open(self.__file_path, 'w', encoding='utf8') as f:
            json.dump(objects, f, ensure_ascii=False)

    def reload(self):
        '''Load the JSON file located at '__file_path' which contains
        JSON form of the <objects> dictionary, deserialize it and
        assign the created dictionary to <__objects>
        '''
        __class__.__objects = {}
        if not os.path.exists(self.__file_path):
            return None

        with open(self.__file_path, 'r', encoding='utf8') as f:
            objects = json.load(f)
        for key, dict_form in objects.items():
            cls_name = dict_form["__class__"]
            self.__objects[key] = globals()[cls_name](**dict_form)
