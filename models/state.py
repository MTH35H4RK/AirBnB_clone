#!/usr/bin/python3
"""This model inherit from BaseModel"""
from models.base_model import BaseModel


class State(BaseModel):
    """Class for state objects."""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initialization of class State"""
        super().__init__(*args, **kwargs)
