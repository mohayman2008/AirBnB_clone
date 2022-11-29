#!/usr/bin/python3
"""Test module for FileStorage class"""

import unittest
import os

from models.engine import file_storage
# from models import storage
from models.engine import classes
FileStorage = file_storage.FileStorage


class TestFileStorage(unittest.TestCase):
    """Tests for FileStorage class"""

    file_path = FileStorage._FileStorage__file_path
    storage = FileStorage()

    def __init__(self, *args, **kwargs):
        '''Constructor'''
        self.remove_json()
        super().__init__(*args, **kwargs)

    def remove_json(self):
        '''Removes the JSON file and reloads'''
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if self.storage.all():
            self.storage.reload()

    def test_class_attributes(self):
        """Tests for the class attributes"""
        self.assertIn("_FileStorage__file_path", dir(FileStorage))
        self.assertIn("_FileStorage__objects", dir(FileStorage))
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)
        # For my own implementation
        self.assertIsInstance(FileStorage._FileStorage__objects_d, dict)
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)
        self.assertEqual(FileStorage._FileStorage__file_path[-5:], '.json')

    def test_all(self):
        """Tests for the method all()"""
        self.assertIsInstance(self.storage.all(), dict)
        self.assertIs(self.storage.all(), FileStorage._FileStorage__objects)

    def test_new(self):
        """Tests for the method new()"""
        self.remove_json()

        for name, cls in classes.items():
            obj = cls()
            index = f'{cls.__name__}.{obj.id}'
            self.assertIn(index, self.storage.all().keys())
            self.assertIn(index, FileStorage._FileStorage__objects.keys())
            self.assertIn(index, FileStorage._FileStorage__objects_d.keys())

            self.assertIs(self.storage.all()[index], obj)
            self.assertIs(FileStorage._FileStorage__objects[index], obj)

            self.assertEqual(FileStorage._FileStorage__objects_d[index],
                             obj.to_dict())
        pass

    def test_save_reload(self):
        """Tests for the methods save() and reload()"""
        self.remove_json()

        self.assertEqual(FileStorage._FileStorage__objects, {})
        self.assertEqual(FileStorage._FileStorage__objects_d, {})

        for name, cls in classes.items():
            obj = cls()
            obj.save()

            FileStorage._FileStorage__objects = {}
            FileStorage._FileStorage__objects_d = {}
            self.storage.reload()

            index = f'{cls.__name__}.{obj.id}'
            self.assertIn(index, self.storage.all().keys())
            self.assertIn(index, FileStorage._FileStorage__objects_d.keys())
            self.assertIn(index, FileStorage._FileStorage__objects.keys())

            self.assertIsNot(self.storage.all()[index], obj)
            self.assertIsNot(FileStorage._FileStorage__objects[index], obj)

            self.assertEqual(FileStorage._FileStorage__objects_d[index],
                             obj.to_dict())
            self.remove_json()
        pass
    pass
