#!/usr/bin/python3
""" User module """
from models.base_model import BaseModel


class User(BaseModel):
    """Inherits from BaseModel and sets attribute"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
