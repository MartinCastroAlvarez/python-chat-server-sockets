"""
Purpose:
This file contains the libraries for creating clients of the chat server.

Author:
Martin Alejandro Castro Alvarez - martincastro.10.5@gmail.com
"""

import logging

from threading import Thread

from .net import HasConnection, HasSocket
from .message import Message
from . import validations

logger: logging.RootLogger = logging.getLogger(__name__)


class Listener(Thread, HasConnection):
    """
    Class responsible for listen for incoming events forever.
    """

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        HasConnection.__init__(self)
        Thread.__init__(self)

    def run(self) -> None:
        """
        Listens for incoming events from the server on the client.
        """
        validations.require_socket(self.connection)
        validations.require_event(self.event)
        try:
            print("Escuchando mensajes del servidor...")
            logger.debug("Listening for messages from the server...")
            for message in self.receive():
                logger.debug('Server says: %s', message.serialize())
                print(message.id, message.text)
        except Exception:
            logger.exception("Exception caught by the listener.")
        self.disconnect()


class Sender(Thread, HasConnection):
    """
    Class responsible for sending messages to the server.
    """

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        HasConnection.__init__(self)
        Thread.__init__(self)

    def run(self) -> None:
        """
        Listens for incoming events from the server on the client.
        """
        validations.require_socket(self.connection)
        validations.require_event(self.event)
        try:
            while self.is_connected():
                logger.debug('Type something:')
                message: Message = Message()
                message.text = input().strip()
                if message.is_quit():
                    break
                if not message.is_empty():
                    self.send(message)
        except Exception:
            logger.exception("Exception caught by the sender.")
        logger.debug('Client disconnected!')
        self.disconnect()


class Client(HasSocket, HasConnection):
    """
    Client class responsinble for connecting to a socket.
    """

    def __init__(self) -> None:
        """
        Lazy constructor.
        """
        HasSocket.__init__(self)
        HasConnection.__init__(self)

    def connect(self) -> None:
        """
        Private method responsible for instantiaing a socket
        that connects to the preconfiugred host and port.
        """
        HasConnection.connect(self)
        try:
            self.connection.connect((self.host, self.port))
        except ConnectionRefusedError:
            logger.debug('Server refused to connect.')
            raise
        else:
            logger.debug("Client connected to %s", self.socket)

    def disconnect(self) -> None:
        """
        Disconnects all threads from the server.
        """
        logger.debug("Client shut down!")
        HasConnection.disconnect(self)
        os._exit(123)

    def start(self) -> None:
        """
        Starts the client thread responsible for listening to incoming
        events from the server and the thread that sends data to the server.
        """
        self.connect()
        # Starting the thread to listen for messages from the server.
        listener: Listener = Listener()
        listener.connection = self.connection
        listener.daemon = True
        listener.start()
        # Starting the thread to send messages to the server.
        sender: Sender = Sender()
        sender.connection = self.connection
        sender.event = listener.event
        sender.start()
