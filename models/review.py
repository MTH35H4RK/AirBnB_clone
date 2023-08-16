#!/usr/bin/python3
"""This model inherit from BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Class for review object."""
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        """Initialization of class Review"""
        super().__init__(*args, **kwargs)
