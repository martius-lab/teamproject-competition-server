"""class for server"""
from typing import Type

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from .server_protocol import COMPServerFactory
from .game import Game

class COMPServer:
    """class for server instance"""

    def __init__(self, GameClass: Type[Game]) -> None:
        self.factory = COMPServerFactory(game_class=GameClass)

    def start(self):
        """set up server at localhost:1234."""
        endpoint = TCP4ServerEndpoint(reactor, 1234)
        endpoint.listen(self.factory)
        print("Server Started")
        reactor.run() # type: ignore[attr-defined]

    def stop(self):
        """terminates server."""
        reactor.stop()