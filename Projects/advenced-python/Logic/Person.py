
from enum import Enum
from abc import ABC, abstractmethod

class State(Enum):
    """
    Represents a state for the Person object.
    """
    state_student = 'Student'
    state_teacher = 'Teacher'
    state_parent = 'Parent'
    state_general_worker = 'General Worker'
    state_manager = 'Manager'



class Person(ABC):
    def __init__(self, name:str, id:str, age:int, phone_number:str, status: State):
        """
        Initializes a Person object with the provided attributes.
        :param name: The name of the person (string, at least 3 characters).
        :param id: The ID of the person (integer, greater than 0).
        :param age: The age of the person (integer, between 18 and 69).
        :param phone_number: The phone number of the person (string, in the format XXX-XXXXXXX).
        :param status: The status of the person (must be an instance of State).
        """
        self.name = name
        self.id = id
        self.age = age
        self.phone_number = phone_number
        self.status = status
#getters and setters
################################################################################################################################
    # Name property
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        """
        Validates and sets the name.
        """
        if len(name) > 1:
            self._name = name
        else:
            raise ValueError("Name must be a string with more than 2 characters.")


    # ID property
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        """
        Validates and sets the ID.
        """
        if len(id)==9 :
            self._id = id
        else:
            raise ValueError("ID must be a 9-digit number.")


    ################################################################################################################################

    # Age property
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        """
        Validates and sets the age.
        """
        if 18 <= age <= 70:
            self._age = age
        else:
            raise ValueError("Age must be a number between 18 and 69.")

    ################################################################################################################################

    # Phone number property
    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        """
        Validates and sets the phone number.
        """

        if len(phone_number)>=9  :
            self._phone_number = phone_number
        else:
            raise ValueError("Phone number must be str and len is 10 . ")

    ################################################################################################################################

    # Status property
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        """
        Validates and sets the status.
        """
        if isinstance(status, State):
            self._status = status
        else:
            raise ValueError("Status must be of type State.")

    ################################################################################################################################

    # __str__ method
    def __str__(self):
        return (f"Person(Name: {self.name}, ID: {self.id}, Age: {self.age}, "
                f"Phone: {self.phone_number}, Status: {self.status})")

    ################################################################################################################################

    # __eq__ method
    def __eq__(self, other):
        """
        Compares two Person objects based on their IDs.
        """
        if isinstance(other, Person):
            return self.id == other.id
        return False


    # This is a polymorphic method, meaning it will be overridden in subclasses.

    @abstractmethod
    def greet(self):
        pass