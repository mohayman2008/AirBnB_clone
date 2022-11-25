#!/usr/bin/python3
""" Review module """
from models.base_model import BaseModel


class Review(BaseModel):
    """Creates attribute for reviews made by users
    about a place
    """
    place_id = ""
    user_id = ""
    text = ""
