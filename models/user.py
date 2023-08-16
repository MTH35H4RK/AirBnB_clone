#!/usr/bin/python3
"""This model inherit from BaseModel"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class for user object."""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """Initialization of class User"""
        super().__init__(*args, **kwargs)
