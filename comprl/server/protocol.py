"""class for server protocol"""

import logging as log
from typing import Callable

from twisted.protocols import amp
from twisted.internet.interfaces import IAddress
from twisted.internet import reactor

from comprl.shared.types import GameID

from ..shared.commands import Auth, StartGame, EndGame, Step, Error

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
        addr: IAddress = self.transport.getPeer()  # type: ignore
        debug_msg = f"connected to client with IP: {addr.host}"
        debug_msg_rest = f", Port: {addr.port} via {addr.type}"
        log.debug(debug_msg + debug_msg_rest)
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

    def get_step(self, obv, return_callback: Callable[[list], None]) -> None:
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
