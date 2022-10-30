#!/usr/bin/python3
"""Airbnb console program."""

import cmd
from models.base_model import BaseModel
from models.user import User
import models
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel(),
        "User": User(),
        "Place": Place(),
        "City": City(),
        "Review": Review(),
        "State": State(),
        "Amenity": Amenity(),
    }

    def do_EOF(self, line):
        """End of file command to exit the program"""
        print("")
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Handles the empty line input"""
        return cmd.Cmd.emptyline(self)

    def postloop(self):
        print()

    def do_create(self, line):
        """Usage: create <class name>"""
        if line is None:
            print("** class name missing **")
            return
        if line not in HBNBCommand.__classes.keys():
            print("** class doesn't exist **")
            return
        else:
            created_object = HBNBCommand.__classes[line]
            created_object.save()
            print(created_object.id)

    def do_show(self, line):
        """usage: show BaseModel 1234-1234-1234"""
        lines = line.split()
        if len(line) == 0:
            print("** class name missing **")
            return
        if lines[0] not in HBNBCommand.__classes.keys():
            print("** class doesn't exist **")
            return

        id_no = lines[1]
        objs = models.storage.all()
        if any(obj.id == id_no for obj in objs.values()):
            print(objs["{}.{}".format(lines[0], id_no)])
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """usage: destroy BaseModel 1234-1234-1234"""
        lines = line.split()
        if len(lines) == 0:
            print("** class name missing **")
            return
        if lines[0] and lines[0] not in HBNBCommand.__classes.keys():
            print("** class doesn't exist **")
            return
        if len(lines) == 1:
            print("** instance id missing **")
        id_no = lines[1]
        objs = models.storage.all()
        if any(obj.id == id_no for obj in objs.values()):
            del objs["{}.{}".format(lines[0], id_no)]
            models.storage.save()
        else:
            print("** no instance id found **")

    def do_all(self, line):
        """usage: all <class name>"""
        lines = line.split()
        if lines[0] and lines[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        new_dict = models.storage.all().values()
        if lines[0]:
            new_arr = []
            for obj in new_dict:
                if obj.__class__.__name__ == lines[0]:
                    new_arr.append(str(obj))
            print(new_arr)
        else:
            new_arr = []
            for obj in new_dict:
                new_arr.append(str(obj))
            print(new_arr)

    def do_update(self, line):
        """usage:update <class name> <id> <attribute name> <attribute value>"""
        lines = line.split()
        if len(lines) == 0:
            print("** class name missing **")
            return
        if lines[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(lines) == 1:
            print("** instance id missing **")
        else:
            objs = models.storage.all()
            id_no = lines[1]
            if not any(obj.id == id_no for obj in objs.values()
                       if obj.__class__.__name__ == lines[0]):
                print("** no instance id found **")
                return
        if len(lines) == 2:
            print("** attribute name missing **")

        if len(lines) == 3:
            try:
                type(eval(lines[2])) != dict
            except NameError:
                print("** value missing **")
                return
        obj = objs["{}.{}".format(lines[0], id_no)]
        if lines[2] not in obj.__class__.__dict__.keys():
            obj.__dict__[lines[2]] = lines[3]
        else:
            lines[3] = type(obj.__class__.__dict__[lines[2]])(lines[3])
            obj.__dict__[lines[2]] = lines[3]
        models.storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
