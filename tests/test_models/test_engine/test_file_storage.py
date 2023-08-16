#!/usr/bin/python3
"""unittests for models/engine/file_storage.py."""
import os
import models
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unit tests to verify the instantiation of the FileStorage class."""

    def case_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def case_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def case_path_type(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def case_objects_type(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def case_storage(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unit tests for FileStorage class methods."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "filetest.json")
        except IOError:
            pass
        self.classes = [
            BaseModel, User,
            State, City,
            Amenity, Place,
            Review
        ]

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
        FileStorage._FileStorage__objects = {}

    def case_all_type(self):
        self.assertEqual(dict, type(models.storage.all()))

    def case_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def case_new(self):
        for cls in self.classes:
            obj = cls()
            models.storage.new(obj)
            key = f"{cls.__name__}.{obj.id}"
            self.assertIn(key, models.storage.all().keys())
            self.assertIn(obj, models.storage.all().values())

    def case_new_args(self):
        for cls in self.classes:
            with self.assertRaises(TypeError):
                models.storage.new(cls(), "hello")

    def case_new_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def case_save(self):
        for cls in self.classes:
            obj = cls()
            models.storage.new(obj)
            models.storage.save()
            with open("file.json", "r") as file:
                text = file.read()
                key = f"{cls.__name__}.{obj.id}"
                self.assertIn(key, text)

    def case_save_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save("HI")

    def case_reload(self):
        for cls in self.classes:
            obj = cls()
            models.storage.new(obj)
            models.storage.save()
            models.storage.reload()
            key = f"{cls.__name__}.{obj.id}"
            reloaded_obj = models.storage.all()[key]
            self.assertIn(key, models.storage.all())

    def case_reload_with_no_file(self):
        try:
            models.storage.reload()
        except FileNotFoundError:
            self.fail()

    def case_reload_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload("Hello")

    def case_save_reload_all_classes(self):
        objs = []
        for cls in self.classes:
            obj = cls()
            objs.append(obj)
            models.storage.new(obj)
            models.storage.save()
            models.storage._FileStorage__objects = {}
            models.storage.reload()

        for obj in objs:
            key = f"{type(obj).__name__}.{obj.id}"
            reloaded_instance = models.storage.all()[key]
            self.assertIsInstance(reloaded_instance, obj.__class__)
            self.assertEqual(reloaded_instance.to_dict(),
                             obj.to_dict())
