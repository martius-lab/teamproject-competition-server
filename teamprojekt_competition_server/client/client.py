from twisted.internet import defer, reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import CommandLocator
from client_protocol import COMPClientProtocol
import sys

sys.path.insert(0, "")
from teamprojekt_competition_server.shared.commands import AuthClient


class COMPClient(CommandLocator):
    def __init__(self, agent) -> None:
        self.connected = False
        self.version = 1
        self.agent = agent

    def connect_client(self, token):
        version = int(1)
        destination = TCP4ClientEndpoint(reactor, "127.0.0.1", 1234)
        auth = connectProtocol(destination, COMPClientProtocol(agent=self.agent))
        auth.addCallback(
            lambda ampProto: ampProto.callRemote(
                AuthClient, token=token, version=version
            )
        )
        defer.DeferredList([auth])
        reactor.run()
