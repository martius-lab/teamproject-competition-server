"""
This is the game logic of a dummy game (rock-paper-scissors).
    0: rock
    1: paper
    2: scissors
"""
from enum import Enum
from .interfaces import IGame, IPlayer

Sign = Enum("Sign", ["ROCK", "PAPER", "SCISSORS"])


class rock_paper_scissors(IGame):
    """
    This class represents a rock-paper-scissors game.
    """

    def __init__(self, players: list[IPlayer]) -> None:
        super().__init__(players=players)
        self.env = list([0.0, 0.0])

    def _update_environment(self):
        player_one_action = self.current_actions[0][0]
        player_two_action = self.current_actions[1][0]
        match player_one_action:
            case Sign.ROCK.value:
                if player_two_action == Sign.SCISSORS.value:
                    self.env[0] += 1
                elif player_two_action == Sign.PAPER.value:
                    self.env[1] += 1
            case Sign.PAPER.value:
                if player_two_action == Sign.ROCK.value:
                    self.env[0] += 1
                elif player_two_action == Sign.SCISSORS.value:
                    self.env[1] += 1
            case Sign.SCISSORS.value:
                if player_two_action == Sign.PAPER.value:
                    self.env[0] += 1
                elif player_two_action == Sign.ROCK.value:
                    self.env[1] += 1

    def _player_won(self, index) -> bool:
        return self.env[index] >= 3

    def _is_finished(self) -> bool:
        return self.env[0] >= 3 or self.env[1] >= 3

    def _observation(self):
        return [float(points) for points in self.env]

    def _validate_action(self, action):
        return 0 <= action and action <= 2

    def _player_stats(self, index) -> int:
        return self.env[index]