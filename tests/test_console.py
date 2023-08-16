#!/usr/bin/python3
"""Defines unittests for console.py."""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class HBNB_Test__promp(unittest.TestCase):
    """Unit tests for evaluation. prompting of the command interpreter."""

    def case_prompt(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def case_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class HBNB_Test__help(unittest.TestCase):
    """Unit tests for evaluation. help messages of the HBNB command interpreter."""

    def case_quit(self):
        prompt_help = ('Exit the program\n'
                       'Usage: quit')
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_EOF(self):
        prompt_help = ('Exit the program with EOF\n'
                       'Usage: EOF (Ctrl+D)')

        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_help(self):
        prompt_help = ('Show help information\n'
                       'Usage: help <command>')
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help help"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_create(self):
        prompt_help = ('Create a new instance of a given class.\n'
                       'Usage: create <class name>')
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_show(self):
        prompt_help = ('Print string representation of an object.\n'
                       'Usage: show <class name> <id>')
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_destroy(self):
        prompt_help = ('Deletes an instance based on the class name and id\n'
                       'Usage: destroy <class name> <id>')
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_all(self):
        prompt_help = ('Prints all string representation of all instances\n'
                       'Usage: all <class name> or all')
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_count(self):
        prompt_help = ('Prints number of instances of a given class.\n'
                       'Usage: count <class name>')
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_update(self):
        prompt_help = ('Updates an instance based on the class name and id\n'
                       'Usage: update <class name> <id> <name> <value>')
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(prompt_help, output.getvalue().strip())

    def case_no_arg(self):
        hlp = "Documented commands (type help <topic>):\n"
        hlp += "========================================\n"
        hlp += "EOF  all  count  create  destroy  help  quit  show  update"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(hlp, output.getvalue().strip())


class HBNB_Test__quit(unittest.TestCase):
    """Unit tests for evaluation. exiting from the HBNB command interpreter."""

    def case_quit(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def case_EOF(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class HBNB_Test__create(unittest.TestCase):
    """Unit tests for evaluation. create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "filetest.json")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("filetest.json", "file.json")
        except IOError:
            pass

    def case_missing_class(self):
        text = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_class(self):
        text = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Ayman"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_syntax1(self):
        text = "*** Unknown syntax: Ayman.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Ayman.create()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_syntax2(self):
        text = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_BaseModeld(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            key1 = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(key1, storage.all().keys())

    def case_User(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            key1 = "User.{}".format(output.getvalue().strip())
            self.assertIn(key1, storage.all().keys())

    def case_State(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            key1 = "State.{}".format(output.getvalue().strip())
            self.assertIn(key1, storage.all().keys())

    def case_City(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            key1 = "City.{}".format(output.getvalue().strip())
            self.assertIn(key1, storage.all().keys())

    def case_Amenity(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            key1 = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(key1, storage.all().keys())

    def case_Place(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            key1 = "Place.{}".format(output.getvalue().strip())
            self.assertIn(key1, storage.all().keys())

    def case_Review(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            key1 = "Review.{}".format(output.getvalue().strip())
            self.assertIn(key1, storage.all().keys())


class HBNB_Test__show(unittest.TestCase):
    """Unit tests for evaluation. show from the HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "filetest.json")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("filetest.json", "file.json")
        except IOError:
            pass

    def case_missing_class(self):
        text = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_class(self):
        text = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_class2(self):
        text = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_missing_id_BaseModel(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_missing_id_User(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_missing_id_State(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_missing_id_City(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_missing_id_Amenity(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_missing_id_Place(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_missing_id_Review(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_instance_BaseModel(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_instance_User(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_instance_State(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(98)"))

    def case_no_instance_City(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_instance_Amenity(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_instance_Place(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_instance_Review(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(98)"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 98"))
            self.assertEqual(text, output.getvalue().strip())

    def case_objects_BaseModel(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "BaseModel.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def case_objects_User(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_id)]
            command = "User.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def case_objects_State(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_id)]
            command = "State.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def case_objects_Place(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "Place.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def case_objects_City(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_id)]
            command = "City.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def case_objects_Amenity(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "Amenity.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def case_objects_Review(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "Review.show({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())


class HBNB_Test__destroy(unittest.TestCase):
    """Unit tests for evaluation. destroy from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "filetest.json")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("filetest.json", "file.json")
        except IOError:
            pass
        storage.reload()

    def case_destroy_missing_class(self):
        text = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_destroy_invalid_class(self):
        text = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Hello"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Hello.destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_BaseModel(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_User(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_State(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_City(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_Amenity(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_Place(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_Review(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_id_BaseModel(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_id_User(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_id_State(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_id_City(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_id_Amenity(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_id_Place(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_id_Review(self):
        text = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 98"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(98)"))
            self.assertEqual(text, output.getvalue().strip())

    def case_BaseModel_objects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "destroy BaseModel {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(test_id)]
            command = "BaseModel.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def case_User_objects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_id)]
            command = "destroy User {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(test_id)]
            command = "User.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def case_State_objects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_id)]
            command = "destroy State {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(test_id)]
            command = "State.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def case_City_objects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_id)]
            command = "destroy City {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(test_id)]
            command = "City.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def case_Amenity_objects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "destroy Amenity {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(test_id)]
            command = "Amenity.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def case_Place_objects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "destroy Place {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(test_id)]
            command = "Place.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def case_Review_objects(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "destroy Review {}".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            test_id = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(test_id)]
            command = "Review.destroy({})".format(test_id)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())


class HBNB_Test__all(unittest.TestCase):
    """Unit tests for evaluation. all of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "filetest.json")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("filetest.json", "file.json")
        except IOError:
            pass

    def case_invalid_class(self):
        text = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_objects_BaseModel(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())

    def case_objects_User(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())

    def case_objects_State(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("State", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())

    def case_objects_Place(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("Place", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())

    def case_objects_City(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("City", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())

    def case_objects_Amenity(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("Amenity", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())

    def case_objects_Review(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("Review", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())

    def case_one_object_BaseModel(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())

    def case_one_object_User(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())

    def case_one_object_State(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())

    def case_one_object_Place(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())

    def case_one_object_City(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())

    def case_one_object_Amenity(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())

    def case_one_object_Review(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertNotIn("BaseModel", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())


class HBNB_Test__update(unittest.TestCase):
    """Unit tests for evaluation. update from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "filetest.json")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("filetest.json", "file.json")
        except IOError:
            pass

    def case_missing_class(self):
        text = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_class(self):
        text = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Hello"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Hello.update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_BaseModel(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_User(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_State(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_City(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_Amenity(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_Place(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_id_Review(self):
        text = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(text, output.getvalue().strip())

    def case_invalid_id_BaseModel(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 98"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(98)"))
            self.assertEqual(correct, output.getvalue().strip())

    def case_invalid_id_User(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User 98"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update(98)"))
            self.assertEqual(correct, output.getvalue().strip())

    def case_invalid_id_State(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State 98"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update(98)"))
            self.assertEqual(correct, output.getvalue().strip())

    def case_invalid_id_City(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City 98"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update(98)"))
            self.assertEqual(correct, output.getvalue().strip())

    def case_invalid_id_Amenity(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 98"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(98)"))
            self.assertEqual(correct, output.getvalue().strip())

    def case_invalid_id_Place(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place 98"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update(98)"))
            self.assertEqual(correct, output.getvalue().strip())

    def case_invalid_id_Review(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review 98"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update(98)"))
            self.assertEqual(correct, output.getvalue().strip())

    def case_no_attr_name_BaseModel(self):
        text = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = output.getvalue().strip()
            command = "update BaseModel {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = output.getvalue().strip()
            command = "BaseModel.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_name_User(self):
        text = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = output.getvalue().strip()
            command = "update User {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = output.getvalue().strip()
            command = "User.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_name_State(self):
        text = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = output.getvalue().strip()
            command = "update State {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = output.getvalue().strip()
            command = "State.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_name_City(self):
        text = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = output.getvalue().strip()
            command = "update City {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = output.getvalue().strip()
            command = "City.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_name_Amenity(self):
        text = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = output.getvalue().strip()
            command = "update Amenity {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = output.getvalue().strip()
            command = "Amenity.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_name_Place(self):
        text = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = output.getvalue().strip()
            command = "update Place {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = output.getvalue().strip()
            command = "Place.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_name_Review(self):
        text = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testId = output.getvalue().strip()
            command = "update Review {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testId = output.getvalue().strip()
            command = "Review.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_value_BaseModel(self):
        text = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "update BaseModel {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "BaseModel.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_value_User(self):
        text = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "update User {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "User.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_value_State(self):
        text = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "update State {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "State.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_value_City(self):
        text = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "update City {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "City.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_value_Amenity(self):
        text = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "update Amenity {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "Amenity.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_value_Place(self):
        text = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "update Place {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "Place.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_no_attr_value_Review(self):
        text = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "update Review {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            command = "Review.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(text, output.getvalue().strip())

    def case_valid_BaseModel(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        command = "update BaseModel {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tId = output.getvalue().strip()
        command = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def case_valid_User(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        command = "update User {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tId = output.getvalue().strip()
        command = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def case_valid_State(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        command = "update State {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tId = output.getvalue().strip()
        command = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def case_valid_City(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        command = "update City {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tId = output.getvalue().strip()
        command = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def case_valid_Amenity(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        command = "update Amenity {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tId = output.getvalue().strip()
        command = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def case_valid_Place(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "update Place {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        command = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def case_valid_Review(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        command = "update Review {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tId = output.getvalue().strip()
        command = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        test_dict = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def case_int(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "update Place {} max_guest 98".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, dic1["max_guest"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        command = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, dic1["max_guest"])

    def case_float(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "update Place {} latitude 7.2".format(testId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(7.2, dic1["latitude"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId = output.getvalue().strip()
        command = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(command))
        dic1 = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, dic1["latitude"])

    def case_dictionary_BaseModel(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        command = "update BaseModel {} ".format(testId)
        command += "'attr_name' 'attr_value'"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            testId = output.getvalue().strip()
        command = "BaseModel.update({}".format(testId)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])

    def case_dictionary_User(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        command = "update User {} ".format(testId)
        command += '"attr_name" "attr value"'
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            testId = output.getvalue().strip()
        command = "User.update({}, ".format(testId)
        command += '{"attr_name": "attr value"})'
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr value", dic1["attr_name"])

    def case_dictionary_State(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        command = "update State {} ".format(testId)
        command += "'attr_name' 'attr_value'"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        command = "State.update({}, ".format(testId)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])

    def case_dictionary_City(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        command = "update City {} ".format(testId)
        command += "'attr_name' 'attr_value'"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            testId = output.getvalue().strip()
        command = "City.update({}, ".format(testId)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])

    def case_dictionary_Place(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "update Place {} ".format(testId)
        command += "'attr_name' 'attr_value'"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "Place.update({}, ".format(testId)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])

    def case_dictionary_ِAmenity(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        command = "update Amenity {} ".format(testId)
        command += "'attr_name' 'attr_value'"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            testId = output.getvalue().strip()
        command = "Amenity.update({}, ".format(testId)
        command += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])

    def case_dictionary_Review(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        command = "update Review {} ".format(testId)
        command += "'attr_name' 'attr_value'"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            testId = output.getvalue().strip()
        command = "Review.update({}, ".format(testId)
        command += '{"attr_name": "attr_value"})'
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", dic1["attr_name"])

    def case_dictionary_int(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "update Place {} ".format(testId)
        command += "max_guest 98"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, dic1["max_guest"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "Place.update({}, ".format(testId)
        command += "{'max_guest': 98})"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, dic1["max_guest"])

    def case_dictionary_with_float(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "update Place {} ".format(testId)
        command += "'latitude' 9.8"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, dic1["latitude"])
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        command = "Place.update({}, ".format(testId)
        command += "{'latitude': 9.8})"
        HBNBCommand().onecmd(command)
        dic1 = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, dic1["latitude"])


class HBNB_Test__count(unittest.TestCase):
    """Unit tests for evaluation. count method of HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "filetest.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("filetest.json", "file.json")
        except IOError:
            pass

    def case_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", output.getvalue().strip())

    def case_BaseModel(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", output.getvalue().strip())

    def case_User(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", output.getvalue().strip())

    def case_State(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", output.getvalue().strip())

    def case_Place(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", output.getvalue().strip())

    def case_City(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", output.getvalue().strip())

    def case_Amenity(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", output.getvalue().strip())

    def case_Review(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", output.getvalue().strip())
