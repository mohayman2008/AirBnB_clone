#!/usr/bin/python3
"""This module contains the difinition of the Place class"""

from . import base_model


class Place(base_model.BaseModel):
    """Class represensts a place"""

    city_id = ''
    user_id = ''
    name = ''
    description = ''
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
    pass
