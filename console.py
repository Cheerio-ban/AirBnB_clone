#!/usr/bin/python3
"""Airbnb console program."""

import cmd


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "


    def do_EOF(self, line):
        """Handles the end of file command"""
        return True

    def do_quit(self, line):
        """Handles quit to exit the program in a clean manner"""
        return True

    def emptyline(self):
        """Handles the empty line input"""
        pass

    def postloop(self):
        print()
















if __name__ == '__main__':
    HBNBCommand().cmdloop()