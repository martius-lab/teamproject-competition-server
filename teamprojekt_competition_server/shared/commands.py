"""
This module defines the commands used for the server client communication.
"""

from twisted.protocols.amp import Integer, String, Boolean, Command, AmpList


class ServerCommand(Command):
    """Interface for commands send from the server"""

    pass


class ClientCommand(Command):
    """Interface for commands send from the client"""

    pass


class AuthFailed(Exception):
    """Exception raised when authentication fails.

    This exception is raised in cases where the authentication process encounters
    an issue, such as an invalid token.

    Attributes:
        None
    """

    pass


class InvalidVersion(Exception):
    """Exception raised for an invalid version during authentication.

    This exception is raised when the version provided during the authentication
    process is not compatible with the current version of the server.

    Attributes:
        None
    """

    pass


class AuthClient(ClientCommand):
    """Command for authenticating the client with the server.

    Arguments:
        token (String): Token of the client
        version (Integer): Version number of the running client framework

    Response:
        uuid (Integer): UUID assigned by the server to the client
    """

    arguments: list[tuple(b"token", String()), tuple(b"version", Integer())]
    response: list[tuple(b"uuid", Integer())]
    fatalErrors: {AuthFailed: b"INVALID_TOKEN", InvalidVersion: b"INCOMPATIBLE_VERSION"}


class StartGame(ServerCommand):
    """Command to notify the client that the game starts"""

    arguments: list[tuple(b"game_id", Integer())]
    response: list[tuple(b"ready", Boolean())]


class EndGame(ServerCommand):
    """Command to notify the client that the game has ended"""

    arguments: list[tuple(b"result", Boolean()), tuple(b"stats", AmpList())]
    response: list[tuple(b"ready", Boolean())]


class Step(ServerCommand):
    """Command for requesting the next step from the agent"""

    arguments: list[tuple(b"env", AmpList())]
    response: list[tuple(b"action", AmpList())]
