"""
Contains all networking related classes and functions for the client.
"""

import logging as log

from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

from comprl.shared.commands import Ready, StartGame, EndGame, Step, Auth, Error, Message

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
        if reactor.running:
            reactor.stop()
        self.agent.on_disconnect()
        return super().connectionLost(reason)

    @Auth.responder
    def auth(self):
        """Called for authenticating the client.

        Returns:
            dict: The client's authentication token and version.
                Example: {"token": b'...', "version": 1}
        """
        return {"token": str.encode(self.agent.auth()), "version": VERSION}

    @Ready.responder
    def ready(self):
        """Called when the server wants to know if the client is ready.

        Returns:
            dict: A dictionary indicating if the client is ready.
                Example: {"ready": True}
        """
        return {"ready": self.agent.is_ready()}

    @StartGame.responder
    def start_game(self, game_id: int):
        """Called when the server starts the game.

        Args:
            game_id (str): The ID of the game.

        Returns:
            dict: A dictionary indicating if the client is ready to start the game.
                Example: {"ready": True}
        """
        self.agent.on_start_game(game_id)
        return {}

    @EndGame.responder
    def end_game(self, result, stats):
        """Called when the server ends the game.

        Args:
            result (bool): A boolean indicating if the game was won.
            stats (object): Other statistics.

        Returns:
            dict: A dictionary indicating if the client is ready to start a new game.
                Example: {"ready": True}
        """
        self.agent.on_end_game(result=result, stats=stats)
        return {}

    @Step.responder
    def step(self, obv: list[float]):
        """Called when the server wants the client to make a step.

        Args:
            obv (list[float])): The environment given by the server.

        Returns:
            dict: A dictionary containing the action that should be executed.
                Example: {"action": 1}
        """
        action = self.agent.get_step(obv)
        if isinstance(action, list) and all(isinstance(x, float) for x in action):
            return {"action": action}
        else:
            raise Exception(
                "Tried to send an action with wrong type. "
                "Only actions of type list[float] can be send."
            )

    @Error.responder
    def on_error(self, msg):
        """Called if an error occurred on the server side.

        Args:
            msg (object): The error description.
        """
        self.agent.on_error(msg=str(msg, encoding="utf-8"))
        return {}

    @Message.responder
    def on_message(self, msg):
        """Called if a message from the server is sent.

        Args:
            msg (object): The message.
        """
        self.agent.on_message(msg=str(msg, encoding="utf-8"))
        return {}


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

    def __on_error(reason):
        agent.on_error(f"Connection to the server failed: {reason}.")
        if reactor.running:
            reactor.stop()

    connectProtocol(
        TCP4ClientEndpoint(reactor, host, port, timeout=30),
        ClientProtocol(agent),
        # we lose the protocol here, is this a problem?
    ).addErrback(__on_error)
    reactor.run()  # type: ignore[attr-defined]
