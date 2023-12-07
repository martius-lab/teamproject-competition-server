""" Hello World """

import asyncio
import logging as log

from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol, ServerFactory

from .protocol import COMPServerProtocol
from .player import COMPPlayer
from .game_manager import GameManager

class COMPServerFactory(ServerFactory):
    """factory for COMP servers"""

    manager : GameManager = GameManager() #TODO: this is hacked, move it into the COMPServer class...

    def buildProtocol(self, addr: IAddress) -> Protocol | None:
        """builds the protocoll"""
        protocol : COMPServerProtocol = COMPServerProtocol()
        
        self.manager.add_player(COMPPlayer(protocol))
        
        return protocol