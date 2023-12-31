"""class for client"""

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import CommandLocator

from .client_protocol import COMPClientProtocol


class COMPClient(CommandLocator):
    """client that manages the connection over the protocol with the server"""

    def __init__(self, agent) -> None:
        self.connected = False
        self.agent = agent

    def connect_client(self, token: str):
        """connects the client to the server

        Args:
            token (str): token to verify the client
        """
        destination = TCP4ClientEndpoint(reactor, "127.0.0.1", 1234)
        connectProtocol(destination, COMPClientProtocol(agent=self.agent, token=token))
        reactor.run()  # type: ignore[attr-defined]
