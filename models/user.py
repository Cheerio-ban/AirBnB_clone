#!/usr/bin/python3

"""
    Represents a user class that inherits fr0m the basemodel class
"""

from models.base_model import BaseModel


class User(BaseModel):
    """User class that inherits the BaseModel"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
