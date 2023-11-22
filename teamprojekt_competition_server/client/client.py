"""class for client"""

from twisted.internet import defer, reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import CommandLocator

from .client_protocol import COMPClientProtocol

from ..shared.commands import AuthClient


class COMPClient(CommandLocator):
    """client that manages the connection over the protocoll with the server"""

    def __init__(self, agent) -> None:
        self.connected = False
        self.version = 1
        self.agent = agent

    def connect_client(self, token: str):
        """connects the client to the server

        Args:
            token (str): token to verify the client
        """
        version = int(1)
        destination = TCP4ClientEndpoint(reactor, "127.0.0.1", 1234)
        auth = connectProtocol(destination, COMPClientProtocol(agent=self.agent))
        auth.addCallback(
            lambda ampProto: ampProto.callRemote(
                AuthClient, token=str.encode(token), version=version
            )
        )
        defer.DeferredList([auth])
        reactor.run()  # type: ignore[attr-defined]
