#!/usr/bin/python3
"""Test module for BaseModel class"""

import unittest
from datetime import datetime
from uuid import uuid4

from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):
    """Tests for BaseModel class"""

    BaseClass = BaseModel
    TestClass = BaseModel
    class_name = "BaseModel"
    attributes = []

    def test_dict_exists(self):
        """Tests for existance of __dict__ attribute"""
        self.assertIn("__dict__", dir(self.TestClass))

    def test_new(self):
        """Test creating new instance of the test class"""
        obj = self.TestClass()
        self.assertEqual(self.TestClass.__name__, self.class_name)
        self.assertIsInstance(obj, self.BaseClass)
        self.assertIsInstance(obj, self.TestClass)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.id, str)

        obj2 = self.TestClass()
        self.assertNotEqual(obj2.created_at, obj.created_at)
        self.assertNotEqual(obj2.updated_at, obj.updated_at)
        self.assertNotEqual(obj2.id, obj.id)

        index_prefix = self.TestClass.__name__ + '.'
        index = index_prefix + obj.id
        self.assertIn(index, storage.all())
        self.assertEqual(obj, storage.all()[index])
        self.assertIs(obj, storage.all()[index])

        index = index_prefix + obj2.id
        self.assertIn(index, storage.all())
        self.assertEqual(obj2, storage.all()[index])
        self.assertIs(obj2, storage.all()[index])

        for name, typ in self.attributes:
            self.assertIsInstance(getattr(obj, name), typ)
        pass

    def test_save_reload(self):
        """Test save and reload"""
        obj = self.TestClass()
        updated_at_old = obj.updated_at
        obj.save()
        self.assertNotEqual(updated_at_old, obj.updated_at)
        index = self.TestClass.__name__ + '.' + obj.id
        self.assertEqual(obj.updated_at, storage.all()[index].updated_at)

        storage.reload()
        self.assertIn(index, storage.all())
        obj_reloaded = storage.all()[index]

        self.assertIsInstance(obj_reloaded, self.BaseClass)
        self.assertIsInstance(obj_reloaded, self.TestClass)
        self.assertIsInstance(obj_reloaded.created_at, datetime)
        self.assertIsInstance(obj_reloaded.updated_at, datetime)
        self.assertIsInstance(obj_reloaded.id, str)

        self.assertEqual(obj.__dict__, obj_reloaded.__dict__)
        self.assertEqual(obj.id, obj_reloaded.id)
        self.assertEqual(obj.created_at, obj_reloaded.created_at)
        self.assertEqual(obj.updated_at, obj_reloaded.updated_at)

        self.assertIsNot(obj, obj_reloaded)

        for name, typ in self.attributes:
            self.assertEqual(getattr(obj, name), getattr(obj_reloaded, name))
            self.assertIsInstance(getattr(obj_reloaded, name),
                                  type(getattr(obj, name)))
        pass

    def test_str(self):
        """Test __str__ method"""
        obj = self.TestClass()
        out = '[{}] ({}) {}'.format(obj.__class__.__name__, obj.id,
                                    obj.__dict__)
        self.assertEqual(str(obj), out)

    def test_to_dict(self):
        """Test to_dict method"""
        obj = self.TestClass()
        obj_d = obj.to_dict()

        self.assertIn("__class__", obj_d)
        self.assertIn("id", obj_d)
        self.assertIn("created_at", obj_d)
        self.assertIn("updated_at", obj_d)

        self.assertEqual(obj_d["__class__"], self.class_name)
        self.assertEqual(obj_d["id"], obj.id)
        self.assertEqual(obj_d["created_at"], obj.created_at.isoformat())
        self.assertEqual(obj_d["updated_at"], obj.updated_at.isoformat())

        self.assertIsInstance(obj_d["__class__"], str)
        self.assertIsInstance(obj_d["id"], str)
        self.assertIsInstance(obj_d["created_at"], str)
        self.assertIsInstance(obj_d["updated_at"], str)

        for key, val in obj.__dict__.items():
            if key not in ("created_at", "updated_at"):
                self.assertEqual(val, getattr(obj, key))
                self.assertIsInstance(val, type(getattr(obj, key)))

        for name, typ in self.attributes:
            if name not in obj.__dict__.keys():
                continue
            self.assertIn(name, obj_d)
            self.assertEqual(obj_d[name], getattr(obj, name))
            self.assertIsInstance(obj_d[name], typ)
    pass
