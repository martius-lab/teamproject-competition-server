"""run a client dummy agent"""

from twisted.internet import reactor
from server_protocol import COMPServerFactory

if __name__ == "__main__":
    pf = COMPServerFactory()
    reactor.listenTCP(1234, pf)
    print("started")
    reactor.run()
