from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.protocol import Factory

from server_protocol import COMPServerProtocol

if __name__ == '__main__':
    pf = Factory()
    pf.protocol = COMPServerProtocol
    reactor.listenTCP(1234, pf)
    print ('started')
    reactor.run()