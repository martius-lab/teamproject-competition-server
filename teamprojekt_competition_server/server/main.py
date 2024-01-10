"""run the server"""
from .server import COMPServer
from .interfaces import IGame, IPlayer
from .game_manager import game_manager
from .databases import GameDatabase


# from .gymgame import GymGame
from .rock_paper_scissors import rock_paper_scissors

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
    game_manager.GameClass = rock_paper_scissors  # GymGame
    server = COMPServer()
    server.start()


def test_database():
    """function to test database"""
    game_db = GameDatabase()
    gameID1 = game_db.insert_game(
        player1_ID=23, player2_ID=4, score_player_1=3, score_player_2=6
    )
    gameID2 = game_db.insert_game(
        player1_ID=43,
        player2_ID=23,
        score_player_1=6,
        score_player_2=7,
        is_player1_winner=False,
    )
    gameID3 = game_db.insert_game(
        player1_ID=23,
        player2_ID=26,
        score_player_1=6,
        score_player_2=7,
        game_end_state=3,
    )
    print(gameID1, gameID2, gameID3)
    print(game_db.get_playerIDs(game_ID=gameID2))
    print(game_db.get_gameIDs(player_ID=23))
    print(game_db.get_won_gameIDs(player_ID=23))


if __name__ == "__main__":
    # main()
    test_database()
