"""
This is the game logic of a dummy game (rock-paper-scissors).
    0: rock
    1: paper
    2: scissors
"""
from .interfaces import IGame, IPlayer


class rock_paper_scissors(IGame):
    """
    This class represents a rock-paper-scissors game.
    """

    def __init__(self, players: list[IPlayer]) -> None:
        super().__init__(players=players)
        self.env = list([0.0, 0.0])

    def _update_environment(self):
        match self.current_actions[0]:
            case 0:  # rock vs.
                if self.current_actions[1] == 2:  # scissors
                    self.env[0] = self.env[0] + 1
                elif self.current_actions[1] == 1:  # paper
                    self.env[1] = self.env[1] + 1
            case 1:  # paper vs.
                if self.current_actions[1] == 0:  # rock
                    self.env[0] = self.env[0] + 1
                elif self.current_actions[1] == 2:  # scissors
                    self.env[1] = self.env[1] + 1
            case 2:  # scissors vs.
                if self.current_actions[1] == 1:  # paper
                    self.env[0] = self.env[0] + 1
                elif self.current_actions[1] == 0:  # rock
                    self.env[1] = self.env[1] + 1

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
