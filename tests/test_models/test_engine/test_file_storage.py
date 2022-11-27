#!/usr/bin/python3
"""Test module for FileStorage class"""

import unittest

from models.engine import file_storage
from models import storage
from models.engine import classes
FileStorage = file_storage.FileStorage


class TestFileStorage(unittest.TestCase):
    """Tests for FileStorage class"""

    def test_class_attributes(self):
        """Tests for the class attributes"""
        self.assertIn("_FileStorage__file_path", dir(FileStorage))
        self.assertIn("_FileStorage__objects", dir(FileStorage))
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)
        self.assertEqual(FileStorage._FileStorage__file_path[-5:], '.json')

    def test_all(self):
        """Tests for the method all()"""
        obj = FileStorage()
        self.assertIsInstance(obj.all(), dict)
        self.assertIs(obj.all(), FileStorage._FileStorage__objects)

    def test_new(self):
        """Tests for the method new()"""
        for name, cls in classes.items():
            obj = cls()

            # self.assertIn()
        pass

    pass
