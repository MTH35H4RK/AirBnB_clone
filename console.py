#!/usr/bin/python3
"""This is code for the AirBnB console"""
import cmd


class HBNBCommand(cmd.Cmd):
    """This is the Console class"""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit is to Exit the program"""
        return True

    def do_EOF(self, arg):
        """This command is to Exit the program with EOF"""
        print()
        return True

    def dohelp(self, arg):
        """This command is to Show help information"""
        super().dohelp(arg)

    def empty_line(self):
        """This Do nothing if an empty line was entered"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
