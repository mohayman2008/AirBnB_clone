#!/usr/bin/python3
"""Test module for User class"""

import unittest

from . import test_base_model
from models.user import User


class TestUser(test_base_model.TestBaseModel):
    """Tests for User class"""

    TestClass = User
    class_name = "User"
    attributes = [("email", str), ("password", str), ("first_name", str),
                  ("last_name", str)]
