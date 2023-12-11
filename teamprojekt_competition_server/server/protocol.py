"""class for server protocol"""

from typing import Callable
import io
from twisted.protocols import amp
from twisted.internet.interfaces import IAddress
from twisted.logger import Logger, textFileLogObserver

from ..shared.commands import Auth, StartGame, EndGame, Step


class COMPServerProtocol(amp.AMP):
    """amp protocol for a COMP server"""
    log = Logger(observer=textFileLogObserver(io.open("./teamprojekt_competition_server/log/server/protocol.log", "a")))
    def __init__(self, boxReceiver=None, locator=None):
        super().__init__(boxReceiver, locator)
        self.connection_made_callbacks : list[Callable[[None], None]] = []
        self.connection_lost_callbacks : list[Callable[[None], None]] = []
        self.log.info("Initialized Protocol: {}".format(id(self)))

    def addConnectionMadeCallback(self, callback):
        self.connection_made_callbacks.append(callback)
    
    def addConnectionLostCallback(self, callback):
        self.connection_lost_callbacks.append(callback)

    def connectionMade(self) -> None:
        addr: IAddress = self.transport.getPeer()  # type: ignore
        print(
            f"Connected to client with IP address: {addr.host}, Port: {addr.port} via {addr.type}"
        )
        #broadcast to callbacks
        for c in self.connection_made_callbacks:
            c()

        return super().connectionMade()
    
    def connectionLost(self, reason):
        
        #broadcast to callbacks
        for c in self.connection_lost_callbacks:
            c()

        return super().connectionLost(reason)

    def get_token(self, return_callback: Callable[[str], None]) -> None:
        """get token from client to authenticate

        Args:
            game (Game): game that starts
        """
        return self.callRemote(Auth).addCallback(
            callback=lambda res: return_callback(res["token"])
        )

    def notify_start(self) -> None:
        """starts the game

        Args:
            game (Game): game that starts
        """
        return self.callRemote(StartGame, game_id=222)

    def get_step(self, obv, return_callback: Callable[[list], None]) -> None:
        """perfroms step requested by player"""

        return self.callRemote(Step, obv=int(obv)).addCallback(
            callback=lambda res: return_callback(res["action"])
        )

    def notify_end(
        self, result, stats, return_callback: Callable[[bool], None]
    ) -> None:
        """ends the game"""

        return self.callRemote(EndGame, result=result, stats=stats).addCallback(
            callback=lambda res: return_callback(res["ready"])
        )
