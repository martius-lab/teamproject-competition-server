"""class for server"""
from twisted.internet import reactor
from server_protocol import COMPServerFactory


class COMPServer:
    """class for server instance"""

    def __init__(self) -> None:
        self.factory = COMPServerFactory()

    def start(self):
        """set up server at localhost:1234."""

        reactor.listenTCP(1234, self.factory)
        reactor.run()

    def stop(self):
        """terminates server."""
        reactor.stop()
