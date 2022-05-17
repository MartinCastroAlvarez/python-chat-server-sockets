"""
Purpose:
This file is used to create a client that connects to a given socket.

Usage:
>>> python3 client.py --host 2018 --host "0.0.0.0" --debug

Author:
Martin Alejandro Castro Alvarez - martincastro.10.5@gmail.com
"""

import sys
import logging

from argparse import ArgumentParser, Namespace, BooleanOptionalAction

from app.client import Client

# Defining command line arguments.
parser: ArgumentParser = ArgumentParser("")
parser.add_argument(
    "--host",
    help="Server hostname.",
    type=str,
    default="127.0.0.1"
)
parser.add_argument(
    "--port",
    help="Server port.",
    type=int,
    default=2018
)
parser.add_argument(
    "--debug",
    help="Enable debug mode.",
    type=bool,
    default=False,
    action=BooleanOptionalAction
)

if __name__ == "__main__":

    # Parsing runtime arguments.
    args: Namespace = parser.parse_args()

    # Enabling debug mode.
    if args.debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Creating client.
    client: Client = Client()
    client.host = "127.0.0.1"
    client.port = 2018
    client.start()
