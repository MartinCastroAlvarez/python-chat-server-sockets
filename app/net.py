"""
Purpose:
This file contains classes to add network functionality to subclasses.

Author:
Martin Alejandro Castro Alvarez - martincastro.10.5@gmail.com
"""

from typing import Generator
from threading import Event, Lock

import logging

import socket

from . import validations
from .message import Message
from .data import Queue

logger: logging.RootLogger = logging.getLogger(__name__)


class HasConnection:
    """
    Class that implements a connection attribute on subclasses.
    """

    BUFFER_SIZE: int = 1024

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        self.__connection: socket.socket = None
        self.__event: Event = Event()

    @property
    def connection(self) -> socket.socket:
        """
        Connection getter.
        """
        return self.__connection

    @connection.setter
    def connection(self, value: socket.socket) -> None:
        """
        Connection setter.
        """
        logger.debug("Setting connection: %s", value)
        validations.require_socket(value)
        self.__connection = value

    @connection.deleter
    def connection(self) -> None:
        """
        Connection deleter.
        """
        logger.debug("Deleting connection: %s", self.connection)
        self.__connection = None

    @property
    def event(self) -> Event:
        """
        Event getter.
        """
        return self.__event

    @event.setter
    def event(self, value: Event) -> None:
        """
        Event setter.
        """
        logger.debug("Setting event: %s", value)
        validations.require_event(value)
        self.__event = value

    @event.deleter
    def event(self) -> None:
        """
        Event deleter.
        """
        logger.debug("Deleting event: %s", self.event)
        self.__event = None

    def connect(self) -> None:
        """
        Creates a new connection.
        Must be overriden by the subclass.
        """
        logger.debug("Opening connection...")
        self.connection = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )

    def disconnect(self) -> None:
        """
        Closes a connection.
        """
        logger.debug("Closing connection...")
        if self.event is not None:
            self.event.set()
            del self.event
        if self.connection is not None:
            self.connection.close()
            del self.connection

    def is_connected(self) -> bool:
        """
        Returns True if connection is still valid.
        """
        return all([
            self.connection is not None,
            self.event is not None and not self.event.is_set(),
        ])

    def receive(self) -> Generator:
        """
        Blocks thread until messages are received.
        """
        logger.debug("Listening...")
        while self.is_connected():
            logger.debug("Waiting for message...")
            try:
                message: Message = Message.unserialize(self.connection.recv(self.BUFFER_SIZE))
            except BrokenPipeError:
                logger.debug("Broken pipe while waiting for messages.")
                self.disconnect()
            except ConnectionResetError:
                logger.debug("Connection reset while waiting for messages.")
                self.disconnect()
            except OSError:
                logger.debug("OS error while waiting for messages.")
                self.disconnect()
            else:
                if message.is_empty():
                    logger.debug("Received empty message.")
                    self.disconnect()
                elif message.is_quit():
                    logger.debug("Received request to quit.")
                    self.disconnect()
                else:
                    logger.debug("Received: %s", message.text)
                    yield message

    def send(self, message: Message) -> None:
        """
        Sends a message to the established connection.
        """
        validations.require_message(message)
        logger.debug("Sending: %s", message.text)
        if self.is_connected():
            try:
                self.connection.send(message.serialize())
            except BrokenPipeError:
                logger.debug("Broken pipe while sending message: %s.", message.text)
                self.disconnect()
            except ConnectionResetError:
                logger.debug("Connection reset while sending message: %s", message.text)
                self.disconnect()
            except OSError:
                logger.debug("OS error while sending message: %s", message.text)
                self.disconnect()


class HasSocket:
    """
    Class that implements host and port attributes on subclasses.
    """

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        self.__host: str = "127.0.0.1"
        self.__port: int = 8000

    @property
    def host(self) -> str:
        """
        Host getter.
        """
        return self.__host

    @host.setter
    def host(self, value: str) -> None:
        """
        Host setter.
        """
        logger.debug("Setting host: %s", value)
        validations.require_non_empty_string(value)
        self.__host = value

    @property
    def port(self) -> int:
        """
        Port getter.
        """
        return self.__port

    @port.setter
    def port(self, value: int) -> None:
        """
        Port setter.
        """
        logger.debug("Setting port: %s", value)
        validations.require_positive_integer(value)
        self.__port = value

    @property
    def socket(self) -> str:
        """
        Socket getter.
        """
        return f'{self.host}:{self.port}'


class HasBuffer:
    """
    Class that implements a buffer for messages attributes on subclasses.
    """

    MAX_SIZE: int = 100

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        self.__buffer: Queue = Queue(Message)
        self.buffer.max_size = self.MAX_SIZE

    @property
    def buffer(self) -> Queue:
        """
        Buffer getter.
        """
        return self.__buffer

    @buffer.setter
    def buffer(self, value: Queue) -> None:
        """
        Buffer setter.
        """
        logger.debug("Setting buffer: %s", value)
        validations.require_queue(value)
        self.__buffer = value


class HasLock:
    """
    Class that implements a lock on subclasses.
    """

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        self.__lock: Lock = Lock()

    @property
    def lock(self) -> Lock:
        """
        Lock getter.
        """
        return self.__lock

    @lock.setter
    def lock(self, value: Lock) -> None:
        """
        Lock setter.
        """
        logger.debug("Setting lock: %s", value)
        validations.require_lock(value)
        self.__lock = value
