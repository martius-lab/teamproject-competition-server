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

    response = [(b"token", String()), (b"version", Integer())]


class StartGame(Command):
    """Command to notify the client that the game starts"""

    arguments = [(b"game_id", Integer())]
    response = [(b"ready", Boolean())]


class EndGame(Command):
    """Command to notify the client that the game has ended"""

    arguments = [
        (b"result", Boolean()),
        (b"stats", Integer()),
    ]
    response = [(b"ready", Boolean())]


class Step(Command):
    """Command for requesting the next step from the agent"""

    arguments = [(b"obv", ListOf(Float()))]
    response = [(b"action", ListOf(Float()))]
