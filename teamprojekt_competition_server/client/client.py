"""class for client"""

import io
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.protocols.amp import CommandLocator
from twisted.logger import Logger, textFileLogObserver
from .client_protocol import COMPClientProtocol


class COMPClient(CommandLocator):
    """client that manages the connection over the protocoll with the server"""

    log = Logger(
        observer=textFileLogObserver(
            io.open("./teamprojekt_competition_server/log/client/client.log", "a")
        )
    )

    def __init__(self, agent) -> None:
        self.connected = False
        self.version = 1
        self.agent = agent
        self.log.info("Inizialized agent: {}".format(id(agent)))
        self.log.info("\t\tversion: {}".format(self.version))

    def connect_client(self, token: str):
        """connects the client to the server

        Args:
            token (str): token to verify the client
        """
        destination = TCP4ClientEndpoint(reactor, "127.0.0.1", 1234)
        auth = connectProtocol(
            destination, COMPClientProtocol(agent=self.agent, token=token)
        )
        print("Connected with token: {}".format(token))
        self.log.info("\t\tConnected with token {}".format(token))
        reactor.run()  # type: ignore[attr-defined]
