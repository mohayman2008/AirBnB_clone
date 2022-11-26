#!/usr/bin/python3
"""This module manages storage and retrieving objects from
a file system storage"""

import json

from . import classes


class FileStorage:
    """Class for managing file system storage"""
    __file_path = "data.json"
    __objects = {}
    __objects_d = {}

    def all(self):
        """Returns a dictionary of all objects"""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the dictionary of objects
        with key <obj class name>.id"""
        key = obj.__class__.__name__ + '.' + obj.id
        val = obj.to_dict()
        if self.__objects.get(key) is None:
            self.__objects[key] = obj
        self.__objects_d[key] = val
        pass

    def save(self):
        """Serializes and saves objects to disk in JSON format"""
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(self.__objects_d, f, ensure_ascii=False)
        pass

    def reload(self):
        """Loads the saved JSON file and deserializes the objects
        to the objects dictionary"""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                self.__objects_d = json.load(f)

            for key, attributes in self.__objects_d.items():
                obj = classes[attributes["__class__"]](**attributes)
                self.__objects[key] = obj
        except FileNotFoundError:
            return

    def remove(self, index):
        """Removes object corresponding <index> from the dictionaries of the
        objects"""
        del self.__objects[index]
        del self.__objects_d[index]
        self.save()
    pass
