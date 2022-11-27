#!/usr/bin/python3
"""Test module for State class"""

import unittest

from . import test_base_model
from models.state import State


class TestState(test_base_model.TestBaseModel):
    """Tests for State class"""

    TestClass = State
    class_name = "State"
    attributes = [("name", str)]
