#!/usr/bin/python3

"""
    Defines all common attributes and methods for all classes
"""

from datetime import datetime
import uuid


class BaseModel:
    """Base model class"""
    def __init__(self):
        """Initializes the BaseModel Class."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __str__(self):
        """Returns a string representation of the base class"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """Updates the updated_at attribute"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns the dictionary of the base model class"""
        base_dict = self.__dict__.copy()
        base_dict['created_at'] = self.created_at.isoformat()
        base_dict['updated_at'] = self.updated_at.isoformat()
        base_dict['__class__'] = self.__class__.__name__
        return base_dict