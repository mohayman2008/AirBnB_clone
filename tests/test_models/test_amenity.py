#!/usr/bin/python3
"""Test module for Amenity class"""

import unittest

from . import test_base_model
from models.amenity import Amenity


class TestAmenity(test_base_model.TestBaseModel):
    """Tests for Amenity class"""

    TestClass = Amenity
    class_name = "Amenity"
    attributes = [("name", str)]
