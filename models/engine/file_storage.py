#!/usr/bin/python3
"""
    Contains class that serializes instances to a json
    file and deserializes json file to instances
"""

import json
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the private class instance dictionary objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets obj parameter name.id as the attribute name to the obj object"""
        FileStorage.__objects["{}.{}".format(obj.to_dict()["__class__"], obj.id)] = obj

    def save(self):
        """Serializes private instance __objects to private instance file_path"""
        save_obj = {}
        for key, value in FileStorage.__objects.items():
            save_obj[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(save_obj, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objdict = json.load(f)
                for elem in objdict.values():
                    cls_name = elem["__class__"]
                    self.new(eval(cls_name)(**elem))
            
        except FileNotFoundError or FileExistsError:
            return

