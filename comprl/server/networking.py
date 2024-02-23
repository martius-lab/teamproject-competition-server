"""contains the networking components of the server"""

import logging as log
from typing import Callable

from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol, ServerFactory
from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from comprl.server.interfaces import IPlayer, IServer
from comprl.server.util import ConfigProvider
from comprl.shared.commands import Auth, EndGame, Error, Ready, StartGame, Step
from comprl.shared.types import GameID

VERSION: int = 1


class COMPServerProtocol(amp.AMP):
    """
    Represents the server-side protocol for the COMP server.

    This class extends the `amp.AMP` class and provides methods for handling
    various events and interactions with the client.

    Attributes:
        connection_made_callbacks (list[Callable[[], None]]): List of callbacks
            to be executed when the connection is made.
        connection_lost_callbacks (list[Callable[[], None]]): List of callbacks
            to be executed when the connection is lost.
    """

    def __init__(self, boxReceiver=None, locator=None):
        super().__init__(boxReceiver, locator)

        self.connection_made_callbacks: list[Callable[[], None]] = []
        self.connection_lost_callbacks: list[Callable[[], None]] = []

    def addConnectionMadeCallback(self, callback):
        """adds callback that is executed, when the connection is made

        Args:
            callback (function): callback to execute, when the connection is made

        Returns:
            None
        """
        self.connection_made_callbacks.append(callback)

    def addConnectionLostCallback(self, callback):
        """
        Adds a callback function to be executed when the connection is lost.

        Args:
            callback: The callback function to be added.

        Returns:
            None
        """
        self.connection_lost_callbacks.append(callback)

    def connectionMade(self) -> None:
        """
        Called when the connection to the client is established.

        Returns:
            None
        """
        # broadcast to callbacks
        for c in self.connection_made_callbacks:
            c()

        return super().connectionMade()

    def connectionLost(self, reason):
        """
        Called when the connection to the client is lost.

        Args:
            reason: The reason for the connection loss.

        Returns:
            None
        """
        log.debug("connection to client lost")
        for c in self.connection_lost_callbacks:
            c()

        super().connectionLost(reason)

    def connectionTimeout(self, failure, timeout) -> None:
        """
        Handles the timeout event for a connection.

        Args:
            failure: The failure object representing the timeout.
            timeout: The timeout value in seconds.
        Returns:
            None
        """
        pass

    def get_token(self, return_callback: Callable[[str], None]) -> None:
        """
        Retrieves a token from the client and calls the return_callback
        function with the token.

        Args:
            return_callback (Callable[[str], None]): A callback function that takes
            a string parameter.

        Returns:
            None
        """

        def callback(res):
            if res["version"] == VERSION:
                return_callback(res["token"].decode())
            else:
                log.error("Client with wrong version tried to authenticate.")
                self.send_error(msg="Tried to connect with wrong version")
                self.disconnect()

        return (
            self.callRemote(Auth)
            .addCallback(callback=callback)
            .addTimeout(ConfigProvider.get("timeout"), reactor, self.connectionTimeout)
            .addErrback(self.handle_remote_error)
        )

    def is_ready(self, return_callback: Callable[[bool], None]) -> bool:
        """
        Checks if the client is ready.

        Args:
            return_callback (Callable[[bool], None]): A callback function that will
            be called with the result of the check.

        Returns:
            bool: Containing the information if the client is ready.
        """
        return (
            self.callRemote(Ready)
            .addCallback(callback=lambda res: return_callback(res["ready"]))
            .addTimeout(ConfigProvider.get("timeout"), reactor, self.connectionTimeout)
            .addErrback(self.handle_remote_error)
        )

    def notify_start(self, game_id: GameID) -> None:
        """
        Notifies the client that a game has started.

        Args:
            game_id (GameID): The ID of the game that has started.
        """
        return self.callRemote(StartGame, game_id=game_id.bytes)

    def get_step(
        self, obv: list[float], return_callback: Callable[[list], None]
    ) -> None:
        """
        Sends an observation to the remote client and retrieves the corresponding
        action.

        Args:
            obv (list[float]): The observation to send to the client.
            return_callback (Callable[[list], None]): The callback function to be
                called with the retrieved action.

        Returns:
            None
        """
        return (
            self.callRemote(Step, obv=obv)
            .addCallback(callback=lambda res: return_callback(res["action"]))
            .addTimeout(ConfigProvider.get("timeout"), reactor, self.connectionTimeout)
            .addErrback(self.handle_remote_error)
        )

    def notify_end(self, result, stats) -> None:
        """
        Notifies the remote client about the end of the game.

        Args:
            result: The result of the game.
            stats: The statistics of the game.

        Returns:
            None
        """
        return (
            self.callRemote(EndGame, result=result, stats=stats)
            .addTimeout(ConfigProvider.get("timeout"), reactor, self.connectionTimeout)
            .addErrback(self.handle_remote_error)
        )

    def send_error(self, msg: str):
        """
        Send an error string to the client.

        Args:
            msg (str): The error message to send.

        Returns:
            None
        """
        return self.callRemote(Error, msg=str.encode(msg)).addErrback(
            self.handle_remote_error
        )

    def disconnect(self):
        """
        Disconnects the client from the server.

        Returns:
            None
        """
        self.transport.loseConnection()

    def handle_remote_error(place, error):
        """Is called when an error in Deferred occurs

        Args:
            place : where the error was caused
            error : description of the error
        """
        log.debug(f"Caught error in remote Callback at {place}")


class COMPPlayer(IPlayer):
    """Represents a player in the COMP game.

    Attributes:
        connection (COMPServerProtocol): The networking connection for the player.
    """

    def __init__(self, connection: COMPServerProtocol) -> None:
        """Initialize the COMPPlayer instance.

        Args:
            connection (COMPServerProtocol): The networking connection for the player.
        """
        super().__init__()
        self.connection: COMPServerProtocol = connection

    def authenticate(self, result_callback):
        """Authenticates the player.

        Args:
            result_callback (callback function):
                The callback to handle the authentication result.

        Returns:
            token (string): The authentication token.
        """
        self.connection.get_token(result_callback)

    def is_ready(self, result_callback) -> bool:
        """Checks if the player is ready to play.

        Args:
            result_callback (callback function): The callback to handle the result.

        Returns:
            bool: True if the player is ready to play, False otherwise.
        """
        return self.connection.is_ready(result_callback)

    def notify_start(self, game_id: GameID):
        """Notifies the player about the start of the game.

        Args:
            game_id (GameID): The ID of the game.
        """
        self.connection.notify_start(game_id=game_id)

    def get_action(self, obv, result_callback):
        """Receives the action from the server.

        Args:
            obv (any): The observation.
            result_callback (callback function): The callback to handle the result.
        """
        self.connection.get_step(obv, result_callback)

    def notify_end(self, result, stats):
        """Called when the game ends.

        Args:
            result (any): The result of the game.
            stats (any): The stats of the game.
        """
        self.connection.notify_end(result=result, stats=stats)

    def disconnect(self, reason: str):
        """Disconnects the player.

        Args:
            reason (str): The reason for the disconnection.
        """
        self.connection.send_error(reason)
        self.connection.disconnect()

    def notify_error(self, error: str):
        """Notifies the player of an error.

        Args:
            error (str): The error message.
        """
        self.connection.send_error(error)


class COMPFactory(ServerFactory):
    """Factory for COMP servers.

    This class represents a factory for creating COMP servers.
    It is responsible for starting and stopping the server, as well as building
    the protocol for incoming connections.

    Attributes:
        server (IServer): The server instance associated with this factory.
    """

    def __init__(self, server: IServer) -> None:
        self.server: IServer = server

    def startFactory(self) -> None:
        """Start the server factory."""
        self.server.on_start()
        super().startFactory()

    def stopFactory(self) -> None:
        """Stop the server factory."""
        self.server.on_stop()
        super().stopFactory()

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        """Build the protocol for incoming connections.

        Args:
            addr (IAddress): The address of the incoming connection.

        Returns:
            Protocol | None: The protocol for the incoming connection.

        """
        protocol: COMPServerProtocol = COMPServerProtocol()
        comp_player: COMPPlayer = COMPPlayer(protocol)

        # set up the callbacks needed for the server
        protocol.addConnectionMadeCallback(lambda: self.server.on_connect(comp_player))
        protocol.addConnectionLostCallback(
            lambda: self.server.on_disconnect(comp_player)
        )

        return protocol


def launch_server(server: IServer, port: int = 65335) -> None:
    """Create a COMP server.

    Args:
        server (IServer): The server instance to be used.
        port (int): The port number of the server. Defaults to 65335.

    """
    log.info(f"Launching server on port {port}")

    reactor.listenTCP(port, COMPFactory(server))  # type: ignore[attr-defined]

    # setup and link the on_update event
    LoopingCall(server.on_update).start(1.0)
    reactor.run()  # type: ignore[attr-defined]
