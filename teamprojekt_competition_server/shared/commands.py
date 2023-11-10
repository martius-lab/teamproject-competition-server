from twisted.protocols.amp import Integer, String, Boolean, Command, AmpList

# Auth/Connetion-Stuff


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


class AuthClient(Command):
    """[CLIENT] Command for authenticating the client with the server.

    Arguments:
        token (String): Token of the client
        version (Integer): Version number of the running client framework 
    
    Response:
        uuid (Integer): UUID assigned by the server to the client
    """
    arguments: [(b"token", String()), (b"version", Integer())]
    response: [(b"uuid", Integer())]
    fatalErrors: {AuthFailed: "invalid-token", InvalidVersion: "invalid-version"}


# Game-Handling


class StartGame(Command):
    """[SERVER] Command to notify the client that the game starts
    """
    arguments: [(b"game_id", Integer())]
    response: [(b"ready", Boolean())]


class EndGame(Command):
    """[SERVER] Command to notify the client that the game has ended
    """
    arguments: [(b"result", Boolean()), (b"stats", AmpList())]
    response: [(b"ready", Boolean())]


# class InvalidUUID(Exception):
#     pass

# class InvalidSurrender(Exception):
#     pass

# class Surrender(Command):
#     arguments: [(b"uuid", Integer())]
#     response: [(b"accepted", Boolean())]
#     errors: {InvalidSurrender: "invalid-surrender"}
#     fatalErrors: {InvalidUUID: "invalid-uuid"}

# Agent


class Step(Command):
    """[SERVER] Command for requesting the next step from the agent
    """
    arguments: [(b"env", AmpList())]
    response: [(b"action", AmpList())]
