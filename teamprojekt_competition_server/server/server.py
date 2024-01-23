"""class for server"""

import logging as log
from typing import Type

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from .factory import COMPServerFactory
from .interfaces import IGame
from . import game_manager

PORT = 65335  # TODO move this in config


class COMPServer:
    """class for server instance"""

    def __init__(self, game_type: Type[IGame]) -> None:
        game_manager.set_game_type(game_type)
        self.factory = COMPServerFactory()
        self.is_running = False

    def start(self) -> None:
        """starts the server, so we can wait for clients to connect"""

        port = PORT
        self.endpoint = TCP4ServerEndpoint(reactor, port)
        self.endpoint.listen(self.factory)
        log.debug(f"Server listening on port {port}")  # TODO some more info here
        self.is_running = True
        reactor.run()  # type: ignore[attr-defined]

    def stop(self) -> None:
        """terminates server."""
        if self.is_running:
            log.debug("Server Stopped")
            reactor.stop()  # type: ignore[attr-defined]
            self.is_running = False

    def __del__(self):
        pass  # TODO: cleanup here ?
