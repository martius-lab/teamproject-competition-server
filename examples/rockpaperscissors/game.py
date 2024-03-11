"""
This is the game logic of a dummy game (rock-paper-scissors).
    0: rock
    1: paper
    2: scissors
"""

from enum import IntEnum

from comprl.server.interfaces import IGame, IPlayer
from comprl.shared.types import PlayerID

Sign = IntEnum("Sign", ["ROCK", "PAPER", "SCISSORS"])


class RPSGame(IGame):
    """
    This class represents a rock-paper-scissors game.
    """

    def __init__(self, players: list[IPlayer]) -> None:
        super().__init__(players=players)

        self.player_1_id = players[0].id
        self.player_2_id = players[1].id

    def _update(self, actions_dict: dict[PlayerID, list[float]]) -> bool:
        player_one_action = int(actions_dict[self.player_1_id][0])
        player_two_action = int(actions_dict[self.player_2_id][0])

        if player_one_action == player_two_action:
            return False  # Tie, no score update

        match player_one_action:
            case Sign.ROCK.value:
                if player_two_action == Sign.SCISSORS.value:
                    self.scores[self.player_1_id] += 1
                elif player_two_action == Sign.PAPER.value:
                    self.scores[self.player_2_id] += 1
            case Sign.PAPER.value:
                if player_two_action == Sign.ROCK.value:
                    self.scores[self.player_1_id] += 1
                elif player_two_action == Sign.SCISSORS.value:
                    self.scores[self.player_2_id] += 1
            case Sign.SCISSORS.value:
                if player_two_action == Sign.PAPER.value:
                    self.scores[self.player_1_id] += 1
                elif player_two_action == Sign.ROCK.value:
                    self.scores[self.player_2_id] += 1

        return max(self.scores[self.player_1_id], self.scores[self.player_2_id]) >= 3

    def _player_won(self, id: PlayerID) -> bool:
        if id == self.player_1_id:
            return self.scores[self.player_1_id] >= 3
        elif id == self.player_2_id:
            return self.scores[self.player_2_id] >= 3
        else:
            return False

    def _get_observation(self, id: PlayerID) -> list[float]:
        if id == self.player_1_id:
            return [self.scores[self.player_1_id]]
        elif id == self.player_2_id:
            return [self.scores[self.player_2_id]]
        else:
            return []

    def _validate_action(self, action) -> bool:
        if len(action) < 1:
            return False
        action = action[0]
        return 0 <= action and action <= 2

    def _player_stats(self, id: PlayerID) -> list[float]:
        other_id = self.player_1_id if self.player_1_id != id else self.player_2_id
        return [self.scores[id], self.scores[other_id]]
