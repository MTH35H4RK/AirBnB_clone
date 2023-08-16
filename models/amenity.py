#!/usr/bin/python3
"""This model inherit from BaseModel"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """A class for representing amenity objects."""
    name = ""

    def __init__(self, *args, **kwargs):
        """Creating an instance of the Amenity class."""
        super().__init__(*args, **kwargs)
