"""run the server"""

from .server import COMPServer
from .interfaces import IGame, IPlayer

import logging
logging.basicConfig(level = logging.DEBUG)

# run with "python -m teamprojekt_competition_server.server.main"

if __name__ == "__main__":

    class ExampleGame(IGame):
        def __init__(self, players: list[IPlayer]) -> None:
            super().__init__(players=players)
            self.env = 0

        async def _game_cycle(self):
            for p in self.players:
                self.env += await p.get_action()
        
        async def _validate_action(self, action):
            return isinstance(action, int)
        
        async def _is_finished(self) -> bool:
            return self.env > 10

    server = COMPServer()
    server.start()
