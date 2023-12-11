"""class for server"""
import io
from twisted.logger import Logger, textFileLogObserver
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from .factory import COMPServerFactory


class COMPServer:
    """class for server instance"""
    log = Logger(observer=textFileLogObserver(io.open("./teamprojekt_competition_server/log/server/server.log", "a")))

    def __init__(self) -> None:
        self.factory = COMPServerFactory()
        self.log.info("COMPServer {} initialized with factory: {}".format(id(self),id(self.factory)))

    def start(self):
        """set up server at localhost:1234."""
        self.endpoint = TCP4ServerEndpoint(
            reactor, 1234
        )  # TODO the port should be in some .env file or so
        self.endpoint.listen(self.factory)
        print("Server Started, listing to localhost:1234")  # TODO some more info here
        self.log.info("\t\tServer: {} now listening to localhost:1234".format(id(self)))
        reactor.run()  # type: ignore[attr-defined]
        self.log.info("\t\tReactor running")

    def stop(self):
        """terminates server."""
        print("Server terminated")
        self.log.info("\t\tTerminated server")
        reactor.stop()
