"""
Contains all networking related classes and functions for the client.
"""

import logging as log

from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

from ..shared.commands import StartGame, EndGame, Step, Auth, Error

from .interfaces import IAgent

VERSION = 1


class ClientProtocol(amp.AMP):
    """Protocol for the client.

    Represents the protocol used by the client to communicate with the server.
    """

    def __init__(self, agent: IAgent, boxReceiver=None, locator=None):
        """Initialize the COMPClientProtocol.

        Args:
            agent (COMPAgent): The agent associated with the protocol.
            boxReceiver (object, optional): The box receiver object. Defaults to None.
            locator (object, optional): The locator object. Defaults to None.
        """
        super().__init__(boxReceiver, locator)
        self.agent: IAgent = agent

    def connectionMade(self):
        """Called when the connection to the server is made."""
        log.debug("Connected to server")
        return super().connectionMade()

    def connectionLost(self, reason):
        """Called when the connection to the server is lost.

        Args:
            reason (object): The reason for the lost connection.
        """
        log.debug(f"Disconnected from the server. Reason: {reason}")
        return super().connectionLost(reason)

    def auth(self):
        """Called for authenticating the client.

        Returns:
            dict: The client's authentication token and version.
                Example: {"token": b'...', "version": 1}
        """
        return {"token": str.encode(self.agent.auth()), "version": VERSION}

    Auth.responder(auth)

    def start_game(self, game_id: int):
        """Called when the server starts the game.

        Args:
            game_id (str): The ID of the game.

        Returns:
            dict: A dictionary indicating if the client is ready to start the game.
                Example: {"ready": True}
        """
        self.agent.on_start_game(game_id)
        return {"ready": True}  # dummy, ready to return to queue

    StartGame.responder(start_game)

    def end_game(self, result, stats):
        """Called when the server ends the game.

        Args:
            result (bool): A boolean indicating if the game was won.
            stats (object): Other statistics.

        Returns:
            dict: A dictionary indicating if the client is ready to start a new game.
                Example: {"ready": True}
        """
        return {
            "ready": self.agent.on_end_game(result=result, stats=stats)
        }  # dummy ready

    EndGame.responder(end_game)

    def step(self, obv):
        """Called when the server wants the client to make a step.

        Args:
            obv (int): The environment given by the server.

        Returns:
            dict: A dictionary containing the action that should be executed.
                Example: {"action": 1}
        """
        return {"action": self.agent.step(obv=obv)}

    Step.responder(step)

    def error(self, msg):
        """Called if an error occurred on the server side.

        Args:
            msg (object): The error description.
        """
        self.agent.on_error(msg=msg)

    Error.responder(error)


def connect_agent(agent: IAgent, host: str = "localhost", port: int = 65335):
    """Connects the client to the server.

    This method connects the client to the server using the specified token, host,
    and port. It internally calls the `run` method of the base class to establish
    the connection.

    Args:
        token (str): The token used for authentication.
        host (str): The host address of the server. Defaults to "localhost".
        port (int): The port number of the server. Defaults to 65335.

    Returns:
        None

    """
    connectProtocol(
        TCP4ClientEndpoint(reactor, host, port),
        ClientProtocol(agent),
        # we lose the protocol here, is this a problem?
    )
    reactor.run()  # type: ignore[attr-defined]
