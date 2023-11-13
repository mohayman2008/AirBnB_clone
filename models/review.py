#!/usr/bin/python3
"""This module contains the difinition of the Review class"""

from . import base_model


class Review(base_model.BaseModel):
    """Class represensts a review for a place"""

    place_id = ''
    user_id = ''
    text = ''
    pass
