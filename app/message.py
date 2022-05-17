"""
Purpose:
This file contains the libraries for creating chat servers.

Author:
Martin Alejandro Castro Alvarez - martincastro.10.5@gmail.com
"""

import time
import logging
from enum import Enum

from .data import HasId
from . import validations

logger: logging.RootLogger = logging.getLogger(__name__)


class Protocol:
    """
    Class that defines protocol constants.
    """

    QUIT: str = "quit"


class Version(Enum):
    """
    Message versioning.
    """
    V1: str = "v1"


class Message(HasId):
    """
    This class represents a message sent to and from the server.
    """

    SEPARATOR: str = "######"

    def __init__(self) -> None:
        """
        Lazy constructor
        """
        HasId.__init__(self)
        self.__text: str = ''
        self.__version: Version = Version.V1
        self.__created_at: int = int(time.time())

    def serialize(self) -> bytes:
        """
        Serializes the message.
        """
        return self.SEPARATOR.join([
            self.version.value,
            str(self.created_at),
            str(self.id),
            self.text,
        ]).encode('utf-8')

    @classmethod
    def unserialize(cls, serialized: bytes) -> 'Message':
        """
        Unserializes the message.
        """
        validations.require_bytes(serialized)
        message: cls = cls()
        parts: list = serialized.decode('utf-8').split(cls.SEPARATOR)
        if parts[0] == Version.V1.value:
            logger.debug('Message v1: %s', serialized)
            message.version = Version.V1
            message.created_at = int(parts[1])
            message.id = int(parts[2])
            message.text = parts[3]
        else:
            logger.debug('Unrecognized message: %s', serialized)
        return message

    @property
    def created_at(self) -> int:
        """
        Creation date getter.
        """
        return self.__created_at

    @created_at.setter
    def created_at(self, value: str) -> str:
        """
        Creation date getter.
        """
        logger.debug('Setting creation date: %s', value)
        validations.require_positive_integer(value)
        self.__created_at: int = value

    @property
    def version(self) -> Version:
        """
        Version getter.
        """
        return self.__version

    @version.setter
    def version(self, value: Version) -> None:
        """
        Creation date getter.
        """
        logger.debug('Setting version: %s', value)
        self.__version: Version = value

    @property
    def text(self) -> str:
        """
        Text getter.
        """
        return self.__text

    @text.setter
    def text(self, value: str) -> str:
        """
        Text getter.
        """
        logger.debug('Setting message text: %s', value)
        if isinstance(value, bytes):
            value: str = value.decode('utf-8')
        validations.require_string(value)
        if self.SEPARATOR in value:
            raise ValueError(f"String contains invalid separator: {value}")
        self.__text: str = value

    def is_quit(self) -> bool:
        """
        Returns True if the message is a request to close the connection.
        """
        return self.text == Protocol.QUIT

    def is_empty(self) -> bool:
        """
        Returns True if the message is empty.
        """
        return not bool(self.text)
