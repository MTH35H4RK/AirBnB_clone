#!/usr/bin/python3
"""This program is for the console"""
import cmd
import re
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
import shlex


allowed_classes = [
    "BaseModel", "User", "State",
    "Place", "City", "Amenity", "Review"
    ]


def error(args):
    if not args:
        print("** class name missing **")
        return True

    if args[0] not in allowed_classes:
        print("** class doesn't exist **")
        return True

    if len(args) < 2:
        print("** instance id missing **")
        return True

    key = f"{args[0]}.{args[1]}"
    if key not in storage.all().keys():
        print("** no instance found **")
        return True
    return False


class HBNBCommand(cmd.Cmd):
    """Console class"""
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """
Exit the program
Usage: quit
"""
        return True

    def do_EOF(self, arg):
        """
Exit the program with EOF
Usage: EOF (Ctrl+D)
"""
        print()
        return True

    def do_help(self, arg):
        """
Show help information
Usage: help <command>
"""
        super().do_help(arg)

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_create(self, class_name):
        """
Create a new instance of a given class.
Usage: create <class name>
"""
        if not class_name:
            print("** class name missing **")
            return
        if class_name in allowed_classes:
            obj = eval(class_name)()
            print(obj.id)
            storage.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
Print string representation of an object.
Usage: show <class name> <id>
"""
        args = arg.split()
        if error(args):
            return
        key = f"{args[0]}.{args[1]}"
        print(storage.all()[key])

    def do_destroy(self, arg):
        """
Deletes an instance based on the class name and id
Usage: destroy <class name> <id>
"""
        args = arg.split()
        if error(args):
            return
        key = f"{args[0]}.{args[1]}"
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """
Prints all string representation of all instances
Usage: all <class name> or all
"""
        lst = []
        if not arg:
            for value in storage.all().values():
                lst.append(str(value))
        elif arg not in allowed_classes:
            print("** class doesn't exist **")
            return
        else:
            for key, value in storage.all().items():
                if arg in key:
                    lst.append(str(value))
        print(lst)

    def do_update(self, arg):
        """
Updates an instance based on the class name and id
Usage: update <class name> <id> <name> <value>
"""
        args = shlex.split(arg)
        if error(args):
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all().keys():
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        obj = storage.all()[key]
        if args[2] in obj.__class__.__dict__.keys():
            att_type = type(obj.__class__.__dict__[args[2]])
            obj.__dict__[args[2]] = att_type(args[3])
        else:
            obj.__dict__[args[2]] = args[3]
        obj.save()

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        methods = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
        }
        args = re.split(r'(?<!\d)\.(?!\d)', arg)
        if len(args) != 2:
            print(f"*** Unknown syntax: {arg}")
            return
        command = args[1].split("(")
        if len(args[0]) == 0 and command[0] in methods.keys():
            print("** class name missing **")
            return
        if len(command) != 2 or command[0] not in methods.keys():
            print(f"*** Unknown syntax: {arg}")
        elif command[1][-1] != ")":
            print(f"*** Unknown syntax: {arg}")
        elif args[0] not in allowed_classes and command[0] != "count":
            print("** class doesn't exist **")
        else:
            command[1] = command[1][:-1]
            mydict = re.search(r"\{(.*?)\}", command[1])
            if mydict is None:
                split_parts = shlex.split(command[1])
            else:
                split_parts = shlex.split(command[1][:mydict.span()[0]])
            split_parts = [i.strip(",") for i in split_parts]
            split_parts = [f'"{s}"' if ' ' in s else s for s in split_parts]
            split_parts = ' '.join(split_parts)
            if split_parts:
                para = f"{args[0]} {split_parts}"
            else:
                para = args[0]
            if mydict is None:
                methods[command[0]](para)
            else:
                input_str = command[1][mydict.span()[0]:mydict.span()[1]]
                input_str = input_str.replace("'", '"')
                myargs = json.loads(input_str)
                for key, value in myargs.items():
                    if type(value) == str and ' ' in value:
                        value = f'"{value}"'
                    methods[command[0]](f"{para} {key} {value}")

    def do_count(self, arg):
        """
Prints number of instances of a given class.
Usage: count <class name>
"""
        count = 0
        for key in storage.all().keys():
            if arg in key:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
