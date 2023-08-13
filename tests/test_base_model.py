#!/usr/bin/python3
# You are looking at the test suite for the BaseModel class.

import os
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class case_testBaseModel(unittest.TestCase):
    """unit tests confirming the proper instantiation of BaseModel class."""

    def case_testno_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def case_testid_type(self):
        self.assertEqual(str, type(BaseModel().id))

    def case_testcreated_at_type(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def case_testupdated_at_type(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def case_testunique_ids(self):
        first = BaseModel()
        second = BaseModel()
        self.assertNotEqual(first.id, second.id)

    def case_testdifferent_created_at(self):
        first = BaseModel()
        sleep(0.1)
        second = BaseModel()
        self.assertLess(first.created_at, second.created_at)

    def case_testdifferent_updated_at(self):
        first = BaseModel()
        sleep(0.1)
        second = BaseModel()
        self.assertLess(first.updated_at, second.updated_at)

    def case_teststr(self):
        date = datetime.today()
        date_repr = repr(date)
        base = BaseModel()
        base.id = "123456"
        base.created_at = base.updated_at = date
        base_str = base.__str__()
        self.assertIn("[BaseModel] (123456)", base_str)
        self.assertIn("'id': '123456'", base_str)
        self.assertIn("'created_at': " + date_repr, base_str)
        self.assertIn("'updated_at': " + date_repr, base_str)

    def case_testargs(self):
        base = BaseModel(None)
        self.assertNotIn(None, base.__dict__.values())

    def case_testkwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        base = BaseModel(id="345", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(base.id, "345")
        self.assertEqual(base.created_at, date)
        self.assertEqual(base.updated_at, date)

    def case_testNone_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def case_testargs_and_kwargs(self):
        date = datetime.today()
        iso = date.isoformat()
        base = BaseModel("12", id="345", created_at=iso, updated_at=iso)
        self.assertEqual(base.id, "345")
        self.assertEqual(base.created_at, date)
        self.assertEqual(base.updated_at, date)


class case_Testsave(unittest.TestCase):
    """assess the functionality of method within the BaseModel."""

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

    def case_testsave1(self):
        base = BaseModel()
        sleep(0.1)
        first = base.updated_at
        base.save()
        self.assertLess(first, base.updated_at)

    def case_testsave2(self):
        base = BaseModel()
        sleep(0.1)
        first = base.updated_at
        base.save()
        second = base.updated_at
        self.assertLess(first, second)
        sleep(0.05)
        base.save()
        self.assertLess(second, base.updated_at)

    def case_testsave_arg(self):
        base = BaseModel()
        with self.assertRaises(TypeError):
            base.save(None)

    def case_testsave_file(self):
        base = BaseModel()
        base.save()
        key = "BaseModel." + base.id
        with open("file.json", "r") as file:
            self.assertIn(key, file.read())


class case_Testto_dict(unittest.TestCase):
    """Unit tests for evaluating the to_dict method of the BaseModel class."""

    def case_testto_dict_type(self):
        base = BaseModel()
        self.assertTrue(dict, type(base.to_dict()))

    def case_testto_dict_keys(self):
        base = BaseModel()
        self.assertIn("id", base.to_dict())
        self.assertIn("created_at", base.to_dict())
        self.assertIn("updated_at", base.to_dict())
        self.assertIn("__class__", base.to_dict())

    def case_testto_dict_with_attributes(self):
        base = BaseModel()
        base.name1 = "Ayman"
        base.name2 = "Karim"
        base.my_number = 98
        self.assertIn("name1", base.to_dict())
        self.assertIn("name2", base.to_dict())
        self.assertIn("my_number", base.to_dict())

    def case_testto_dict_datetime_type(self):
        base = BaseModel()
        base_dict = base.to_dict()
        self.assertEqual(str, type(base_dict["created_at"]))
        self.assertEqual(str, type(base_dict["updated_at"]))

    def case_testto_dict(self):
        date = datetime.today()
        base = BaseModel()
        base.id = "12345"
        base.created_at = base.updated_at = date
        dict_base = {
            'id': '12345',
            '__class__': 'BaseModel',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat()
        }
        self.assertDictEqual(base.to_dict(), dict_base)

    def case_testdict_vs_to_dict(self):
        base = BaseModel()
        self.assertNotEqual(base.to_dict(), base.__dict__)

    def case_testto_dict_with_arg(self):
        base = BaseModel()
        with self.assertRaises(TypeError):
            base.to_dict("hello")
