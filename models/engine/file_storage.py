#!/usr/bin/python3
""""This class is responsible for  serializing,deserializing JSON files. """
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage():
    """"This class serializes and deserializes JSON files."""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the __objects directory """
        return self.__objects

    def new(self, obj):
        """"Sets in  the obj __objects with <obj class name>.id key """
        self.__objects[f"{type(obj).__name__}.{obj.id}"] = obj

    def save(self):
        """"Converting __objects into JSON format and saving to a file. """
        objs = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w") as file:
            json.dump(objs, file)

    def reload(self):
        """"Parsing JSON data from a file into a dictionary of __objects."""
        try:
            with open(FileStorage.__file_path) as file:
                objs = json.load(file)
                for obj in objs.values():
                    class_name = obj["__class__"]
                    self.new(eval(class_name)(**obj))
        except FileNotFoundError:
            return
