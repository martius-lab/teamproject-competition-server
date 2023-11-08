from twisted.protocols.amp import Integer, String, Boolean, Command, AmpList

# Auth/Connetion-Stuff

class AuthFailed(Exception):
    pass


class InvalidVersion(Exception):
    pass


class AuthClient(Command):
    arguments: [(b"token", String()), (b"version", Integer())]
    response: [(b"uuid", Integer())]
    fatalErrors: {AuthFailed: "invalid-token", InvalidVersion: "invalid-version"}


# Game-Handling


class StartGame(Command):
    arguments: [(b"game_id", Integer())]
    response: [(b"ready", Boolean())]


class EndGame(Command):
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
    arguments: [(b"env", AmpList())]
    response: [(b"action", AmpList())]
