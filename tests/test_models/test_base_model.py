#!/usr/bin/python3
'''Unitests for the BaseModel class or an inheriting child class
'''
from datetime import datetime
import unittest
import uuid

from models.base_model import BaseModel
from models import storage


class TestBaseModel(unittest.TestCase):
    '''TestCase class for the BaseModel class or a child class
    '''
    TestClass = BaseModel
    attributes = ()

    def test_init(self):
        '''Testing initialization of a BaseModel object'''

        obj1 = self.TestClass()

        self.assertIsInstance(obj1, self.TestClass)
        self.assertIsInstance(obj1, BaseModel)

        self.assertIsInstance(obj1.id, str)
        self.assertEqual(len(obj1.id), len(str(uuid.uuid4())))
        for obj in (obj1.created_at, obj1.updated_at):
            self.assertIsInstance(obj, datetime)

        obj2 = self.TestClass()
        self.assertNotEqual(obj1.id, obj2.id)

        id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        updated_at = datetime.now().isoformat()
        num = 15
        a_list = [(1, 'a'), 1.5]
        obj_dict = {"id": id, "created_at": created_at,
                    "updated_at": updated_at, "num": num, "a_list": a_list,
                    "__class__": "SomeClass"}

        obj3 = self.TestClass(**obj_dict)
        for key, val in obj_dict.items():
            if key == "__class__":
                continue
            elif key in ("created_at", "updated_at"):
                attrib_val = getattr(obj3, key)
                self.assertIsInstance(attrib_val, datetime)
                self.assertEqual(attrib_val, datetime.fromisoformat(val))
            else:
                attrib_val = getattr(obj3, key)
                self.assertIsInstance(attrib_val, type(val))
                self.assertEqual(attrib_val, val)

        obj4 = self.TestClass(**obj1.to_dict())
        self.assertTrue(obj4 is not obj1)

        for attrib in ("id", "created_at", "updated_at"):
            attrib_val = getattr(obj4, attrib, None)
            self.assertIsNotNone(attrib_val)

    def test_to_dict(self):
        '''Testing to_dict(self) method'''

        obj1 = self.TestClass()
        dict1 = obj1.to_dict()

        self.assertIsInstance(dict1, dict)

        keys = dict1.keys()
        for key in obj1.__dict__.keys().__and__(("__class__",)):
            self.assertIn(key, keys)
            self.assertIsInstance(dict1[key], str)

        for attrib in ("created_at", "updated_at"):
            self.assertEqual(dict1[attrib], getattr(obj1, attrib).isoformat())
        self.assertEqual(dict1["id"], obj1.id)
        self.assertEqual(dict1["__class__"], self.TestClass.__name__)

    def test_str(self):
        '''Testing __str__(self) method'''
        obj1 = self.TestClass()
        str1 = obj1.__str__()

        self.assertEqual(str1, str(obj1))
        str_regex = "\\[{}\\] \\({}\\) {{.*}}"
        self.assertRegex(str1, str_regex.format(self.TestClass.__name__,
                                                obj1.id))

    def test_save(self):
        '''Testing to_dict(self) method'''
        obj1 = self.TestClass()
        old_updated_at = obj1.updated_at
        obj1.save()
        self.assertNotEqual(obj1.updated_at, old_updated_at)
        self.assertIn(f"{obj1.__class__.__name__}.{obj1.id}",
                      storage.all().keys())

    def test_class_attributes(self):
        '''Testing class attributes'''
        for attr_name, attr_type in self.attributes:
            self.assertIn(attr_name, dir(self.TestClass))
            self.assertIsInstance(getattr(self.TestClass, attr_name),
                                  attr_type)
