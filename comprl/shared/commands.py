"""
Defines the commands used for the server client communication.
"""

from twisted.protocols.amp import Integer, String, Boolean, Command, Float, ListOf


class Auth(Command):
    """Command for authenticating the client with the server.

    Arguments:
        token (String): Token of the client
        version (Integer): Version number of the running client framework

    Response:
        uuid (Integer): UUID assigned by the server to the client
    """

    arguments = []
    response = [(b"token", String()), (b"version", Integer())]


class Ready(Command):
    """Command to check if the client is ready to start the game"""

    arguments = []
    response = [(b"ready", Boolean())]


class StartGame(Command):
    """Command to notify the client that the game starts"""

    arguments = [(b"game_id", String())]
    response = []


class EndGame(Command):
    """Command to notify the client that the game has ended"""

    arguments = [
        (b"result", Boolean()),
        (b"stats", ListOf(Float())),
    ]
    response = []


class Step(Command):
    """Command for requesting the next step from the agent"""

    arguments = [(b"obv", ListOf(Float()))]
    response = [(b"action", ListOf(Float()))]


class Error(Command):
    """Command interface for a generic error message"""

    arguments = [(b"msg", String())]
    response = []


class Message(Command):
    """Command interface for a generic message"""

    arguments = [(b"msg", String())]
    response = []
