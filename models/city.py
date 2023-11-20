#!/usr/bin/python3
"""
Defines the City class.
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    A blueprint for a City object
    """

    state_id = ""
    name = ""
