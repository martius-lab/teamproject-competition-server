"""run the server"""

from .server import COMPServer
from .interfaces import IGame, IPlayer

from .game_manager import game_manager

import logging

logging.basicConfig(level=logging.DEBUG)

# run with "python -m teamprojekt_competition_server.server.main"


class ExampleGame(IGame):
    def __init__(self, players: list[IPlayer]) -> None:
        super().__init__(players=players)
        self.env = 0

    def _update_enviroment(self):
        self.env += sum(self.current_actions)

    def _validate_action(self, action):
        return isinstance(action, int)

    def _is_finished(self) -> bool:
        return self.env > 10
    
    def _observation(self):
        return self.env
    
    def _player_stats(self, index) -> int:
        return 0
    
    def _player_won(self, index) -> bool:
        if index==0: return True
        return False


def main():
    game_manager.GameClass = ExampleGame
    server = COMPServer()
    server.start()


if __name__ == "__main__":
    main()
