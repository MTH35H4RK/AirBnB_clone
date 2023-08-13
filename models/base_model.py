#!/usr/bin/python3
# You are viewing the code for the BaseModel class.
import uuid
from datetime import datetime
import models


class BaseModel():
    """The foundational model that serves as the basis for all other models."""
    def __init__(self, *args, **kwargs):
        """The process of initializing or setting up the BaseModel class."""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, date)
                elif key == "__class__":
                    pass
                else:
                    setattr(self, key, value)
        models.storage.new(self)

    def __str__(self):
        """Provide the string representation of the class."""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Store the updated date."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Provide a dictionary representing the class."""
        data_dict = self.__dict__.copy()
        data_dict['created_at'] = data_dict['created_at'].isoformat()
        data_dict['updated_at'] = data_dict['updated_at'].isoformat()
        data_dict['__class__'] = self.__class__.__name__
        return data_dict
