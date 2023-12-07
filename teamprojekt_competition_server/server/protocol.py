"""class for server protocol"""
import asyncio
import logging as log

from twisted.protocols import amp

from ..shared.commands import Auth, StartGame, EndGame, Step
from ..shared.twisted_asyncio import twisted_async


class COMPServerProtocol(amp.AMP):
    """amp protocol for a COMP server"""

    def __init__(self, boxReceiver=None, locator=None):
        super().__init__(boxReceiver, locator)

    def connectionLost(self, reason) -> None:
        """is called when a client disconnects"""

        # TODO handle this!

        return super().connectionLost(reason)

    def connectionMade(self):
        log.debug("Client connected")
        test = self.get_token()
        print(test)
        return super().connectionMade()

    async def get_token(self) -> str:
        token = await self.callRemote(Auth)
        log.debug(token)
        return token

    async def notify_start(self) -> bool:
        """starts the game

        Args:
            game (Game): game that starts
        """
        return await self.callRemote(StartGame, game_id=222).asFuture(loop=asyncio.get_event_loop())

    async def get_step(self, obv):
        """perfroms step requested by player"""

        return await self.callRemote(Step, obv=int(obv)).asFuture(loop=asyncio.get_event_loop())

    async def notify_end(self, result, stats) -> bool:
        """ends the game"""
        
        return await self.callRemote(EndGame, result=True, stats=4).asFuture(loop=asyncio.get_event_loop())
