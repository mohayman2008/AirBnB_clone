#!/usr/bin/python3
"""This module contains the difinition of the User class"""

from . import base_model


class User(base_model.BaseModel):
    """Class represensts users"""

    email = ''
    password = ''
    first_name = ''
    last_name = ''
    pass
