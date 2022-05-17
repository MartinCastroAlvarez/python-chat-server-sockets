"""
Purpose:
This file contains classes to implement data structures.

Author:
Martin Alejandro Castro Alvarez - martincastro.10.5@gmail.com
"""

import logging
from typing import Generator

from . import validations

logger: logging.RootLogger = logging.getLogger(__name__)


class HasId:
    """
    Class that implements an ID attribute on subclasses.
    """

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        self.__id: int = -1

    @property
    def id(self) -> int:
        """
        ID getter.
        """
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        """
        ID setter.
        """
        logger.debug("Setting id: %s", value)
        validations.require_integer(value)
        self.__id = value


class Map:
    """
    HashMap implementation in Python.
    """

    def __init__(self, data_type: type = str) -> None:
        """
        Lazy constructor.
        """
        self.__data: dict = {}
        self.__type: type = data_type

    @property
    def data(self) -> dict:
        """
        Raw data getter.
        """
        return self.__data

    def add(self, value: object) -> None:
        """
        Adds a new element to the HashMap.
        """
        logger.debug("Adding to Map(%s): %s", self.__type, value)
        if not isinstance(value, self.__type):
            raise TypeError(f"Expecting {self.__type}, got {type(self.value)}")
        if not isinstance(value, HasId):
            raise TypeError(f"{value} is not a subclass of HasId")
        self.data[value.id] = value

    def remove(self, value: int) -> None:
        """
        Removes an element from the HashMap.
        """
        logger.debug("Removing from Map(%s): %s", self.__type, value)
        validations.require_integer(value)
        if self.has(value):
            del self.data[value]

    def has(self, value: int) -> bool:
        """
        Returns True if ID is in the data.
        """
        return value in self.data

    def all(self) -> Generator:
        """
        Returns all the elements in the hashmap.
        """
        yield from [
            *self.data.values()
        ]

    def keys(self) -> Generator:
        """
        Returns all the element ids in the hashmap.
        """
        yield from self.data.keys()

    def size(self) -> int:
        """
        Returns the size of the HashMap.
        """
        return len(self.data)

    def is_empty(self) -> bool:
        """
        Returns True if the HashMap is empty.
        """
        return len(self.data) == 0


class Array:
    """
    Array implementation in Python.
    """

    def __init__(self, data_type: type = str) -> None:
        """
        Lazy constructor.
        """
        self.__data: list = []
        self.__type: type = data_type
        self.__max_size: int = 0

    @property
    def data(self) -> list:
        """
        Raw data getter.
        """
        return self.__data

    def add(self, value: object) -> None:
        """
        Adds a new element to the HashMap.
        """
        logger.debug("Adding to Array(%s): %s", self.__type, value)
        if not isinstance(value, self.__type):
            raise TypeError(f"Expecting {self.__type}, got {type(self.value)}")
        self.data.append(value)

    def all(self) -> Generator:
        """
        Returns all the elements in the hashmap.
        """
        yield from [*self.data]

    def size(self) -> int:
        """
        Returns the size of the HashMap.
        """
        return len(self.data)

    @property
    def max_size(self) -> int:
        """
        Max size getter.
        """
        return self.__max_size

    @max_size.setter
    def max_size(self, value: int) -> None:
        """
        Max size setter.
        """
        logger.debug("Setting array max size: %s", value)
        validations.require_positive_integer(value)
        self.__max_size = value

    def is_empty(self) -> bool:
        """
        Returns True if the Array is empty.
        """
        return len(self.data) == 0


class Queue(Array):
    """
    Queue implementation in Python.
    """

    def pop(self) -> object:
        """
        Fetches and removes one element from the queue.
        """
        return self.data.pop()

    def push(self, *args, **kwargs) -> None:
        """
        Adds an element to the queue.
        """
        self.add(*args, **kwargs)
