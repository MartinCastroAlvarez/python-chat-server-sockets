"""
Purpose:
This file contains the libraries for creating chat servers.

Author:
Martin Alejandro Castro Alvarez - martincastro.10.5@gmail.com
"""

import os
import time
import logging

import socket
from threading import Thread

from .net import HasConnection, HasSocket, HasBuffer, HasLock
from .message import Message
from .data import HasId, Map
from . import validations

logger: logging.RootLogger = logging.getLogger(__name__)


class Sender(Thread, HasConnection, HasId, HasBuffer):
    """
    Thread class responsible for sending messages to clients.
    """

    SLEEP: float = 0.5

    def __init__(self) -> None:
        """
        Lazy constructor
        """
        Thread.__init__(self)
        HasConnection.__init__(self)
        HasId.__init__(self)
        HasBuffer.__init__(self)

    def run(self) -> None:
        """
        Method responsible for handling sending messages to the client.
        """
        logger.debug("Client #%s connected!", self.id)
        validations.require_positive_integer(self.id)
        validations.require_socket(self.connection)
        while self.is_connected():
            while not self.buffer.is_empty() and self.is_connected():
                message: Message = self.buffer.pop()
                logger.debug("Sending to #%s: %s", self.id, message.text)
                if not message.is_empty():
                    self.send(message)
            time.sleep(self.SLEEP)
        logger.debug("Client #%s disconnected from sender", self.id)
        self.disconnect()


class Listener(Thread, HasConnection, HasId, HasBuffer, HasLock):
    """
    Thread class responsible for handling requests from clients.
    """

    def __init__(self) -> None:
        """
        Lazy constructor
        """
        Thread.__init__(self)
        HasConnection.__init__(self)
        HasId.__init__(self)
        HasBuffer.__init__(self)
        HasLock.__init__(self)

    def run(self) -> None:
        """
        Method responsible for handling incoming messages from the client.
        """
        logger.debug("Client #%s connected!", self.id)
        validations.require_positive_integer(self.id)
        validations.require_socket(self.connection)
        for message in self.receive():
            message.id = self.id
            logger.debug("Client #%s says: %s", message.id, message.text)
            print(message.id, message.text)
            # Adding message to the queue of messages.
            self.lock.acquire()
            self.buffer.push(message)
            self.lock.release()
        logger.debug("Client #%s disconnected from listener", self.id)
        self.disconnect()


class Monitor(Thread, HasConnection, HasBuffer, HasLock):
    """
    Thread class responsible for pushing messages to clients.
    """

    SLEEP: float = 0.5

    def __init__(self) -> None:
        """
        Lazy constructor
        """
        Thread.__init__(self)
        HasConnection.__init__(self)
        HasBuffer.__init__(self)
        HasLock.__init__(self)
        self.senders: Map = Map(Sender)
        self.listeners: Map = Map(Listener)

    def disconnect(self) -> None:
        """
        Disconnects all clients from this server.
        """
        for listener in self.listeners.all():
            logger.debug("Disconnecting listener #%s", listener.id)
            listener.disconnect()
        for sender in self.senders.all():
            logger.debug("Disconnecting sender #%s", sender.id)
            sender.disconnect()
        logger.debug("Monitor shut down!")
        HasConnection.disconnect(self)
        os._exit(123)

    def __dispatch(self) -> None:
        """
        Extracting client messages from the server buffer.
        """
        logger.debug("Monitor has %s message(s)", self.buffer.size())
        while not self.buffer.is_empty() and self.is_connected():
            message: Message = self.buffer.pop()
            for sender in self.senders.all():
                logger.debug("Assigning to #%s: %s", message.id, message.text)
                sender.buffer.push(message)

    def __groom(self) -> None:
        """
        Removing disconnected clients.
        """
        logger.debug("There are %s client(s) connected", self.senders.size())
        for sender in self.senders.all():
            if not sender.is_connected():
                logger.debug("Removing disconnected client #%s", sender.id)
                self.senders.remove(sender.id)
                self.listeners.remove(sender.id)

    def run(self) -> None:
        """
        Method responsible for assigning messages to all clients.
        """
        logger.debug("Monitor started!")
        validations.require_socket(self.connection)
        while self.is_connected():
            self.__groom()
            self.__dispatch()
            time.sleep(self.SLEEP)
        logger.debug("Server disconnected on the monitor.")
        self.disconnect()
        os._exit(324)


class Server(HasSocket, HasConnection):
    """
    Server class responsinble for listening on a socket.
    """

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        HasSocket.__init__(self)
        HasConnection.__init__(self)
        self.monitor: Monitor = Monitor()

    def connect(self) -> None:
        """
        Private method responsible for instantiaing a socket
        that listens on the preconfiugred host and port.
        """
        HasConnection.connect(self)
        self.connection.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )
        self.connection.bind((self.host, self.port))
        self.connection.listen(1)
        logger.debug("Server listening on %s", self.socket)

    def start(self) -> None:
        """
        Starts the server on the preconfigured socket.
        """
        self.connect()
        # Starting the monitoring thread.
        self.monitor.connection = self.connection
        self.monitor.start()
        # Blocking and waiting for connections from clients.
        try:
            while self.is_connected():
                logger.debug("Waiting for client message..")
                client_socket, client_address = self.connection.accept()
                self.__handle(client_socket, client_address)
        except KeyboardInterrupt:
            logger.debug("Disconnecting server because of keyboard interruption.")
        self.disconnect()

    def __handle(self, sock: socket.socket, address: tuple) -> None:
        """
        Registers a new client.
        """
        logger.debug("Connected with: %s", address)
        print("Nuevo client:", address)
        # Creating a new sender to send messages to this client.
        sender: Sender = Sender()
        sender.connection = sock
        sender.id = address[1]
        # Creating a new listener to receive messages from this client.
        listener: Listener = Listener()
        listener.connection = sock
        listener.event = sender.event
        # The listener and the sender share the same id.
        listener.id = address[1]
        # All listeners share the same buffer.
        listener.buffer = self.monitor.buffer
        # All listeners share the same lock.
        listener.lock = self.monitor.lock
        # Registering sender and listener in this server.
        self.monitor.senders.add(sender)
        self.monitor.listeners.add(listener)
        # Starting sender and listener for this client.
        sender.start()
        listener.start()
