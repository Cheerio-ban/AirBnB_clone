#!/usr/bin/python3
"""Airbnb console module."""
import cmd
from models.base_model import BaseModel
from models.user import User
import models
import json
import shlex
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """Represents the console interpreter"""

    prompt = "(hbnb) "
    file = None
    __classes = {
        "BaseModel": BaseModel(),
        "User": User(),
        "Place": Place(),
        "City": City(),
        "Review": Review(),
        "State": State(),
        "Amenity": Amenity(),
    }

    def parse_input(self, line: str):
        """Parses the command line arguments"""
        if '"' in line:
            inp = shlex.split(line)
            inp = [o.strip('"') for o in inp]
            return inp
        inp = line.split(" ")
        return inp

    def default(self, line):
        """This overrides the default command"""
        cmds = {"all()": self.do_all,
                "count()": self.count
                }
        c2 = {"show": self.do_show,
              "destroy": self.do_destroy,
              "update": self.do_update
              }
        ar = line.split(".")
        if "." not in line:
            print("** Unknown syntax: {} **".format(line))
            return
        if ar[1] not in cmds.keys() and ar[1].split("(")[0] not in c2.keys():
            print("** Unknown syntax: {} **".format(line))
            return
        if ar[1] in cmds:
            cmds[ar[1]]("{}".format(ar[0]))
        else:
            if "update" not in ar[1]:
                id = ar[1].split('(')[1].split(')')[0]
                c2[ar[1].split("(")[0]]("{} {}".format(ar[0], id))
            else:
                if "{" not in ar[1]:
                    id = ar[1].split("(")[1].split(",")[0]
                    atr = ar[1].split("(")[1].split(",")[1]
                    al = ar[1].split("(")[1].split(",")[2].split(")")[0]
                    cmd = ar[1].split("(")[0]
                    c2[cmd]('{} {} {} "{}" '.format(ar[0], id, atr, al))
                else:
                    id = ar[1].split("(")[1].split("{")[0].strip(", ")
                    at_d = '{' + ar[1].split("(")[1].split("{")[1].strip(")")
                    cmd = ar[1].split("(")[0]
                    c2[cmd]('{}.{} {}'.format(ar[0], id, at_d))

    def do_EOF(self, line):
        """End of file or ctrl^D command to exit the program"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self) -> None:
        """Handles the empty line input"""
        return

    def do_create(self, line):
        """Usage: create <class name>"""
        if line is None:
            print("** class name missing **")
            return
        if line not in HBNBCommand.__classes.keys():
            print("** class doesn't exist **")
            return
        else:
            created_object = eval(f'{line}()')
            created_object.save()
            print(created_object.id)

    def do_show(self, line):
        """usage: show BaseModel 1234-1234-1234"""
        lines = self.parse_input(line)
        if len(line) == 0:
            print("** class name missing **")
            return
        if lines[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(lines) == 1:
            print("** instance id missing **")
            return
        id_no = lines[1]
        objs = models.storage.all()
        if any(obj.id == id_no for obj in objs.values()):
            print(objs["{}.{}".format(lines[0], id_no)])
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """usage: destroy BaseModel 1234-1234-1234"""
        if len(line) == 0:
            print("** class name missing **")
            return
        lines = self.parse_input(line)
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
            print("** no instance found **")

    def do_all(self, line):
        """usage: all <class name>"""
        lines = self.parse_input(line)
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
        """
        usage: update <class name> <id> <attribute name>
        '<attribute value>'
        """
        if "{" in line:
            ar = line.split(".")
            cls = ar[0]
            id_no = ar[1].split("{")[0].strip(" ")
            at_d = ar[1].split("{")[-1].strip("}")
            at_d = at_d.split(",")
            b = {o.split(":")[0].strip(" '").strip(' "'):
                 o.split(":")[1].strip(" '").strip(' "') for o in at_d}
            objs = models.storage.all()
            if not any(obj.id == id_no for obj in objs.values()
                       if obj.__class__.__name__ == cls):
                print("** no instance found **")
            else:
                obj = objs["{}.{}".format(ar[0], id_no)]
                [setattr(obj, k, v) for k, v in b.items()]
            models.storage.save()
            return
        lines = self.parse_input(line)
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
                print("** no instance found **")
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

    def count(self, line):
        ar = self.parse_input(line)
        print(len([obj for obj in models.storage.all().values()
              if obj.__class__.__name__ == ar[0]]))

    def to_dict(self, obj):
        """Convert @obj to  dict"""
        return eval(obj)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
