from twisted.internet import defer, reactor, protocol
from twisted.internet.task import deferLater
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols import amp
from twisted.protocols.amp import Integer, String, Boolean, Command, AmpList
from client_protocol import COMPClientFactory, COMPClientProtocol
from teamprojekt_competition_server.shared.commands import AuthClient, StartGame, EndGame, Step

class COMPClient():
    def __init__(self, step: callable[int, int]) -> None:
        self.connected = False
        self.version = 1
        self.step = step
        
    
    def connect_client(self, token):
        token = b"ABC" #dummy token
        version = int(1)
        destination = TCP4ClientEndpoint(reactor, "127.0.0.1", 1234)
        auth = connectProtocol(destination, COMPClientProtocol())
        auth.addCallback(lambda ampProto: ampProto.callRemote(AuthClient, token=token, version=version))
        defer.DeferredList([auth])
        reactor.run()