#!/usr/bin/python3
"""Package models"""

from .engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()

__all__ = ["base_model", "amenity", "city", "place", "review", "state",
           "user", "engine"]
