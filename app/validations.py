"""
Purpose:
This file contains utility functions to validate user input.

Author:
Martin Alejandro Castro Alvarez - martincastro.10.5@gmail.com
"""

from threading import Event

import socket

from .data import Queue
from .message import Message


def require_socket(value: socket.socket) -> None:
    """
    Validates that the input is a valid socket.
    """
    if value is None:
        raise ValueError(f"Socket can not be null: {value}")
    if not isinstance(value, socket.socket):
        raise TypeError(f"Expecting socket, got: {type(value)}")


def require_event(value: Event) -> None:
    """
    Validates that an event is valid.
    """
    if value is None:
        raise ValueError(f"Event can not be null: {value}")
    if not isinstance(value, Event):
        raise TypeError(f"Expecting Event, got: {type(value)}")


def require_lock(value: Event) -> None:
    """
    Validates that a lock is valid.
    """
    if value is None:
        raise ValueError(f"Lock can not be null: {value}")
    if value.__class__.__name__ != 'lock':
        raise TypeError(f"Expecting Lock, got: {type(value)}")


def require_queue(value: Queue) -> None:
    """
    Validates that a queue is valid.
    """
    if value is None:
        raise ValueError(f"Queue can not be null: {value}")
    if not isinstance(value, Queue):
        raise TypeError(f"Expecting Queue, got: {type(value)}")


def require_message(value: Message) -> None:
    """
    Validates that a message is valid.
    """
    if value is None:
        raise ValueError(f"Message can not be null: {value}")
    if not isinstance(value, Message):
        raise TypeError(f"Expecting Message, got: {type(value)}")


def require_non_empty_string(value: str) -> None:
    """
    Validates that the input is a valid string.
    """
    if not isinstance(value, str):
        raise TypeError(f"Expecting string, got: {type(value)}")
    require_string(value)


def require_string(value: str) -> None:
    """
    Validates that the input is a valid string.
    """
    if not isinstance(value, str):
        raise TypeError(f"Expecting string, got: {type(value)}")


def require_bytes(value: bytes) -> None:
    """
    Validates that the input is a valid bytes object.
    """
    if not isinstance(value, bytes):
        raise TypeError(f"Expecting bytes, got: {type(value)}")


def require_positive_integer(value: int) -> None:
    """
    Validates that the input is a valid integer.
    """
    require_integer(value)
    if value <= 0:
        raise ValueError(f"Integer must not be negative: {value}.")


def require_integer(value: int) -> None:
    """
    Validates that the input is a valid integer.
    """
    if not isinstance(value, int):
        raise TypeError(f"Expecting integer, got: {type(value)}")
