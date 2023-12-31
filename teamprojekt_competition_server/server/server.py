"""class for server"""

import logging as log

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from .factory import COMPServerFactory


class COMPServer:
    """class for server instance"""

    def __init__(self) -> None:
        self.factory = COMPServerFactory()

    def start(self):
        """set up server at localhost:1234."""
        self.endpoint = TCP4ServerEndpoint(
            reactor, 1234
        )  # TODO the port should be in some .env file or so
        self.endpoint.listen(self.factory)
        log.debug("Server Started")  # TODO some more info here
        reactor.run()  # type: ignore[attr-defined]

    def stop(self):
        """terminates server."""
        log.debug("Server Stopped")
        reactor.stop()
