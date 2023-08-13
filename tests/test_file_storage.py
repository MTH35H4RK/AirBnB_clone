#!/usr/bin/python3
"""the unittests of models/engine/file_storage.py."""
import os
import models
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class FileStorage_Test_init(unittest.TestCase):
    """Unit tests for verifying the instantiation of the FileStorage class."""

    def case_testno_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def case_testwith_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def case_testpath_type(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def case_testobjects_type(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def case_teststorage(self):
        self.assertEqual(type(models.storage), FileStorage)


class FileStorage_methodsofTest(unittest.TestCase):
    """Unit tests to validate the functionality methods within FileStorage."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "filetest.json")
        except IOError:
            pass

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

    def case_testall_type(self):
        self.assertEqual(dict, type(models.storage.all()))

    def case_testwith_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def case_testnew(self):
        base = BaseModel()
        models.storage.new(base)
        self.assertIn("BaseModel." + base.id, models.storage.all().keys())
        self.assertIn(base, models.storage.all().values())

    def case_testnew_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), "hello")

    def case_testnew_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def case_testsave(self):
        base = BaseModel()
        models.storage.new(base)
        models.storage.save()
        with open("file.json", "r") as file:
            text = file.read()
            self.assertIn("BaseModel." + base.id, text)

    def case_testsave_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save("HI")

    def case_testreload(self):
        base = BaseModel()
        models.storage.new(base)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + base.id, objs)

    def case_testreload_no_file(self):
        try:
            models.storage.reload()
        except FileNotFoundError:
            self.fail("Error")

    def case_testreload_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload("HI")
