from twisted.internet import reactor
from server_protocol import COMPServerFactory

class COMPServer():
    def __init__(self) -> None:
        self.factory = COMPServerFactory()
    
    def start(self):
        reactor.listenTCP(1234, self.factory)
        reactor.run()
        
    def stop(self):
        reactor.stop()