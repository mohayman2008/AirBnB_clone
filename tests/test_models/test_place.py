#!/usr/bin/python3
"""Test module for City class"""

import unittest

from . import test_base_model
from models.place import Place


class TestPlace(test_base_model.TestBaseModel):
    """Tests for Place class"""

    TestClass = Place
    class_name = "Place"
    attributes = [("city_id", str), ("user_id", str), ("name", str),
                  ("description", str), ("number_rooms", int),
                  ("number_bathrooms", int), ("max_guest", int),
                  ("price_by_night", int), ("latitude", float),
                  ("longitude", float), ("amenity_ids", list)]
