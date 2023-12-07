"""Player"""

from .protocol import COMPServerProtocol
from .interfaces import IPlayer

from ..shared.twisted_asyncio import twisted_async

class COMPPlayer(IPlayer):
    connection :  COMPServerProtocol
    
    def __init__(self, connection : COMPServerProtocol) -> None:
        self.connection = connection    
    
    async def authenticate(self):
        return await self.connection.get_token()
    
    async def notify_start(self):
        self.connection.notify_start()
    
    async def get_action(self, obv):
        return await self.connection.get_step(obv)
    
    async def notify_end(self):
        return self.connection.notify_end()
    