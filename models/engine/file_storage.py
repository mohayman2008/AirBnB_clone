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
        self.rebuild_objects_d()
        key = obj.__class__.__name__ + '.' + obj.id
        # val = obj.to_dict()
        # if self.__objects.get(key) is None:
        self.__objects[key] = obj
        self.__objects_d[key] = obj.to_dict()
        pass

    def save(self):
        """Serializes and saves objects to disk in JSON format"""
        self.rebuild_objects_d()
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(self.__objects_d, f)
            # json.dump(self.__objects_d, f, ensure_ascii=False)
        pass

    def reload(self):
        """Loads the saved JSON file and deserializes the objects
        to the objects dictionary"""
        self.__class__.__objects = {}
        self.__class__.__objects_d = {}
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                self.__class__.__objects_d = json.load(f)

            for key, attributes in self.__objects_d.items():
                obj = classes[attributes["__class__"]](**attributes)
                self.__objects[key] = obj
        except (FileNotFoundError, Exception):
            return

    def rebuild_objects_d(self):
        '''Rebuilds <FileStorage.__objects_d>'''
        # To be called if <FileStorage.__objects_d> was altered manually
        if self.__objects.keys() != self.__objects_d.keys():
            self.__class__.__objects_d = {}
            for key, obj in self.__objects.items():
                self.__objects_d[key] = obj.to_dict()

    def remove(self, index):
        """Removes object corresponding <index> from the dictionaries of the
        objects"""
        del self.__objects[index]
        del self.__objects_d[index]
        self.save()
    pass
