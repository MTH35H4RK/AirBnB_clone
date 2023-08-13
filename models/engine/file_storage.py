#!/usr/bin/python3
""""This class handles the conversion of data to and from JSON files. """
import json
from models.base_model import BaseModel


class FileStorage():
    """"perform both serialization and deserialization of JSON files."""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Provide the directory named __objects."""
        return self.__objects

    def new(self, obj):
        """"Store object in the __objects with the key <obj class name>.id."""
        self.__objects[f"{type(obj).__name__}.{obj.id}"] = obj

    def save(self):
        """"Serializing the contents of __objects to a JSON file. """
        objs = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w") as file:
            json.dump(objs, file)

    def reload(self):
        """"JSON file into the __objects dictionary through deserialization."""
        try:
            with open(FileStorage.__file_path) as file:
                objs = json.load(file)
                for obj in objs.values():
                    class_name = obj["__class__"]
                    self.new(eval(class_name)(**obj))
        except FileNotFoundError:
            pass
