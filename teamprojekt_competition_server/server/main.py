"""run a client dummy agent"""

from twisted.internet import reactor

from twisted.internet.endpoints import TCP4ServerEndpoint
from .server_protocol import COMPServerFactory


if __name__ == "__main__":
    factory = COMPServerFactory()

    endpoint = TCP4ServerEndpoint(reactor, 1234)
    endpoint.listen(factory)
    print("Server Started")
    reactor.run()  # type: ignore[attr-defined]
