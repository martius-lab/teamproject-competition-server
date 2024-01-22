"""run the server"""

from .server import COMPServer
from .interfaces import IGame, IPlayer
from .databases import GameDatabase


# from .gymgame import GymGame
# from .rock_paper_scissors import rock_paper_scissors
from .laserhockeygame import LaserHockeyGame

import logging

logging.basicConfig(level=logging.DEBUG)

# run with "python -m teamprojekt_competition_server.server.main"


class ExampleGame(IGame):
    """example for a game"""

    def __init__(self, players: list[IPlayer]) -> None:
        super().__init__(players=players)
        self.env = 0

    def _update_environment(self):
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
        if index == 0:
            return True
        return False


def main():
    """main function for testing"""
    server = COMPServer(LaserHockeyGame)
    server.start()


def test_database():
    """function to test database"""
    game_db = GameDatabase()
    gameID = game_db.insert_game(12, 23)
    gameID = game_db.insert_game(52, 12)
    print(gameID)
    print(game_db.get_playerIDs(gameID=gameID))
    print(game_db.get_gameIDs(playerID=12))
    print(game_db.get_won_gameIDs(playerID=12))


if __name__ == "__main__":
    main()
    # test_database()
