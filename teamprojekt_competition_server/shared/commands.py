"""
Defines the commands used for the server client communication.
"""

from twisted.protocols.amp import Integer, String, Boolean, Command


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

    arguments = [(b"game_id", String())]
    response = [(b"ready", Boolean())]


class EndGame(Command):
    """Command to notify the client that the game has ended"""

    arguments = [
        (b"result", Boolean()),
        (b"stats", Integer()),
    ]  # Integer acts as a dummy type, we might want to create a custom data-type here!
    response = [(b"ready", Boolean())]


class Step(Command):
    """Command for requesting the next step from the agent"""

    arguments = [
        (b"obv", Integer())
    ]  # Integer acts as a dummy type, we might want to create a custom data-type here!
    response = [
        (b"action", Integer())
    ]  # Integer acts as a dummy type, we might want to create a custom data-type here!


class Error(Command):
    """Command interface for a generic error message"""

    arguments = [(b"msg", String())]
