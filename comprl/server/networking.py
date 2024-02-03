"""contains the networking components of the server"""

import logging as log
from typing import Callable

from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol, ServerFactory
from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from comprl.server.interfaces import IPlayer, IServer
from comprl.shared.commands import Auth, EndGame, Error, StartGame, Step
from comprl.shared.types import GameID

TIMEOUT = 10

VERSION: int = 1


class COMPServerProtocol(amp.AMP):
    """amp protocol for a COMP server"""

    def __init__(self, boxReceiver=None, locator=None):
        super().__init__(boxReceiver, locator)

        self.connection_made_callbacks: list[Callable[[], None]] = []
        self.connection_lost_callbacks: list[Callable[[], None]] = []

    def addConnectionMadeCallback(self, callback):
        """adds callback that is executed, when the connection is made

        Args:
            callback (function): callback to execute, when the connection is made
        """
        self.connection_made_callbacks.append(callback)

    def addConnectionLostCallback(self, callback):
        """adds callback that is executed, when the connection is lost

        Args:
            callback (function): callback to execute, when the connection is lost
        """
        self.connection_lost_callbacks.append(callback)

    def connectionMade(self) -> None:
        """called upon connectionMade event"""

        # broadcast to callbacks
        for c in self.connection_made_callbacks:
            c()

        return super().connectionMade()

    def connectionLost(self, reason):
        """called upon connectionLost event"""
        log.debug("connection to client lost")
        for c in self.connection_lost_callbacks:
            c()

        return super().connectionLost(reason)

    def connectionTimeout(self, failure, timeout):
        """called upon timeout"""
        pass

    def get_token(self, return_callback: Callable[[str], None]) -> None:
        """get token from client to authenticate

        Args:
            game (Game): game that starts
        """

        def callback(res):
            if res["version"] == VERSION:
                return_callback(res["token"].decode())
            else:
                log.error("Client with wrong version tried to authenticate.")
                self.send_error(msg="Tried to connect with wrong version")
                self.transport.loseConnection()

        self.callRemote(Auth).addCallback(callback=callback).addTimeout(
            TIMEOUT, reactor, self.connectionTimeout
        )

    def notify_start(self, game_id: GameID) -> None:
        """starts the game

        Args:
            game (Game): game that starts
        """
        return self.callRemote(StartGame, game_id=game_id.bytes)

    def get_step(
        self, obv: list[float], return_callback: Callable[[list], None]
    ) -> None:
        """performs step requested by player"""

        return (
            self.callRemote(Step, obv=obv)
            .addCallback(callback=lambda res: return_callback(res["action"]))
            .addTimeout(TIMEOUT, reactor, self.connectionTimeout)
        )

    def notify_end(
        self, result, stats, return_callback: Callable[[bool], None]
    ) -> None:
        """ends the game"""

        return (
            self.callRemote(EndGame, result=result, stats=stats)
            .addCallback(callback=lambda res: return_callback(res["ready"]))
            .addTimeout(TIMEOUT, reactor, self.connectionTimeout)
        )

    def send_error(self, msg: str):
        """send an error string to the client"""
        self.callRemote(Error, msg=str.encode(msg))

    def disconnect(self):
        """disconnects the client from the server"""
        self.transport.loseConnection()


class COMPPlayer(IPlayer):
    """player of the game"""

    def __init__(self, connection: COMPServerProtocol) -> None:
        # init super to obtain id
        super().__init__()

        # set the networing connection
        self.connection: COMPServerProtocol = connection

    def authenticate(self, result_callback):
        """authenticates player

        Args: result_callback (callback function)

        Returns: token (string)"""
        self.connection.get_token(result_callback)

    def notify_start(self, game_id: GameID):
        """notifies start of game"""
        self.connection.notify_start(game_id=game_id)

    def get_action(self, obv, result_callback):
        """receive action from server

        Args:
            obv(any): observation"""
        self.connection.get_step(obv, result_callback)

    def notify_end(self, result, stats):
        """called when game ends

        Args:
            result (any): result of the game
            stats: (any): stats of the game"""

        self.connection.notify_end(
            result=result,
            stats=stats,
            return_callback=lambda res: True,  # TODO: what to do with the result?
        )

    def disconnect(self, reason: str):
        """disconnect the player

        Args:
            reason (str): reason why it disconnects
        """
        self.connection.send_error(reason)
        self.connection.disconnect()

    def notify_error(self, error: str):
        """notifies the player of an error

        Args:
            error (str): error message
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
