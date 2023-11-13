#!/usr/bin/python3
"""Test module for City class"""

import unittest

from . import test_base_model
from models.city import City


class TestCity(test_base_model.TestBaseModel):
    """Tests for City class"""

    TestClass = City
    class_name = "City"
    attributes = [("state_id", str), ("name", str)]
