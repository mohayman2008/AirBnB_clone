#!/usr/bin/python3
"""Test module for Review class"""

import unittest

from . import test_base_model
from models.review import Review


class TestReview(test_base_model.TestBaseModel):
    """Tests for Review class"""

    TestClass = Review
    class_name = "Review"
    attributes = [("place_id", str), ("user_id", str), ("text", str)]
