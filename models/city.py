#!/usr/bin/python3
"""This module contains the difinition of the City class"""

from . import base_model


class City(base_model.BaseModel):
    """Class represensts a City"""

    state_id = ''
    name = ''
    pass
