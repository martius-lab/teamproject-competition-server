""" Hello World """

from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol, ServerFactory

from .protocol import COMPServerProtocol
from .player import COMPPlayer

from . import player_manager


class COMPServerFactory(ServerFactory):
    """factory for COMP servers"""

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        """builds the protocoll"""
        protocol: COMPServerProtocol = COMPServerProtocol()

        new_player = COMPPlayer(protocol)
        player_manager.register(new_player)

        return protocol
