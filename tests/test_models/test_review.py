#!/usr/bin/python3
"""Defines unittests for models/review.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class Review_Test__instantiation(unittest.TestCase):
    """Unittests instantiation of the Review class."""

    def case_no_args(self):
        self.assertEqual(Review, type(Review()))

    def case_Review_storage(self):
        self.assertIn(Review(), models.storage.all().values())

    def case_id_type(self):
        self.assertEqual(str, type(Review().id))

    def case_created_at_type(self):
        self.assertEqual(datetime, type(Review().created_at))

    def case_updated_at_typ(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def case_email_type(self):
        self.assertEqual(str, type(Review.place_id))

    def case_password_type(self):
        self.assertEqual(str, type(Review.user_id))

    def case_first_name_type(self):
        self.assertEqual(str, type(Review.text))

    def case_unique_ids(self):
        Review1 = Review()
        Review2 = Review()
        self.assertNotEqual(Review1.id, Review2.id)

    def case_different_created_at(self):
        Review1 = Review()
        sleep(0.1)
        Review2 = Review()
        self.assertLess(Review1.created_at, Review2.created_at)

    def case_different_updated_at(self):
        Review1 = Review()
        sleep(0.1)
        Review2 = Review()
        self.assertLess(Review1.updated_at, Review2.updated_at)

    def case_str(self):
        date = datetime.today()
        date_repr = repr(date)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = date
        Review_str = review.__str__()
        self.assertIn("[Review] (123456)", Review_str)
        self.assertIn("'id': '123456'", Review_str)
        self.assertIn("'created_at': " + date_repr, Review_str)
        self.assertIn("'updated_at': " + date_repr, Review_str)

    def case_unused_args(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def case_kwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        review = Review(id="345", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, date)
        self.assertEqual(review.updated_at, date)

    def case_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class Review_Test__save(unittest.TestCase):
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
        review = Review()
        sleep(0.1)
        first_updated_at = review.updated_at
        review.save()
        self.assertLess(first_updated_at, review.updated_at)

    def case_saves2(self):
        review = Review()
        sleep(0.1)
        first = review.updated_at
        review.save()
        second = review.updated_at
        self.assertLess(first, second)
        sleep(0.1)
        review.save()
        self.assertLess(second, review.updated_at)

    def case_save_with_arg(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.save("hello")

    def case_file(self):
        review = Review()
        review.save()
        usid = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class Review_Test__to_dict(unittest.TestCase):
    """Unit tests for evaluation. to_dict method of the Review class."""

    def case_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def case_correct_keys(self):
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def case_added_attributes(self):
        review = Review()
        review.middle_name = "Ayman"
        review.number = 98
        self.assertEqual("Ayman", review.middle_name)
        self.assertIn("number", review.to_dict())

    def case_datetime_type(self):
        review = Review()
        Review_dict = review.to_dict()
        self.assertEqual(str, type(Review_dict["id"]))
        self.assertEqual(str, type(Review_dict["created_at"]))
        self.assertEqual(str, type(Review_dict["updated_at"]))

    def case_to_dict_output(self):
        date = datetime.today()
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = date
        Review_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), Review_dict)

    def case_dict_vs_to_dict(self):
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)

    def case_to_dict_with_arg(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)
