#!/usr/bin/python3
"""Package engine: For management of data storage"""

from ..base_model import BaseModel
from ..user import User

classes = {"BaseModel": BaseModel, "User": User}

__all__ = ["file_storage"]
