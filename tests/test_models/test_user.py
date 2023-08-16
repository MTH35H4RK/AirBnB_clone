#!/usr/bin/python3
"""Defines unittests for models/user.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class USER_Test__instantiation(unittest.TestCase):
    """Unit tests for evaluation. instantiation of the User class."""

    def case_no_args(self):
        self.assertEqual(User, type(User()))

    def case_user_storage(self):
        self.assertIn(User(), models.storage.all().values())

    def case_id_type(self):
        self.assertEqual(str, type(User().id))

    def case_created_at_type(self):
        self.assertEqual(datetime, type(User().created_at))

    def case_updated_at_typ(self):
        self.assertEqual(datetime, type(User().updated_at))

    def case_email_type(self):
        self.assertEqual(str, type(User.email))

    def case_password_type(self):
        self.assertEqual(str, type(User.password))

    def case_first_name_type(self):
        self.assertEqual(str, type(User.first_name))

    def case_last_name_type(self):
        self.assertEqual(str, type(User.last_name))

    def case_unique_ids(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def case_different_created_at(self):
        user1 = User()
        sleep(0.1)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def case_different_updated_at(self):
        user1 = User()
        sleep(0.1)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def case_str(self):
        date = datetime.today()
        date_repr = repr(date)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = date
        user_str = user.__str__()
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + date_repr, user_str)
        self.assertIn("'updated_at': " + date_repr, user_str)

    def case_unused_args(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def case_kwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        user = User(id="345", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, date)
        self.assertEqual(user.updated_at, date)

    def case_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class USER_Test__save(unittest.TestCase):
    """Unit tests for evaluation. save method of the  class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def case_save1(self):
        user = User()
        sleep(0.1)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def case_saves2(self):
        user = User()
        sleep(0.1)
        first = user.updated_at
        user.save()
        second = user.updated_at
        self.assertLess(first, second)
        sleep(0.1)
        user.save()
        self.assertLess(second, user.updated_at)

    def case_save_with_arg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save("hello")

    def case_file(self):
        user = User()
        user.save()
        usid = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class USER_Test__to_dict(unittest.TestCase):
    """Unit tests for evaluation. to_dict method of the User class."""

    def case_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def case_correct_keys(self):
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    def case_added_attributes(self):
        user = User()
        user.middle_name = "Ayman"
        user.number = 98
        self.assertEqual("Ayman", user.middle_name)
        self.assertIn("number", user.to_dict())

    def case_datetime_type(self):
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def case_to_dict_output(self):
        date = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = date
        user_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), user_dict)

    def case_contrast_to_dict_dunder_dict(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def case_to_dict_with_arg(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)
