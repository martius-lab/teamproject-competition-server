from comprl.server.interfaces import IGame, IPlayer
from comprl.shared.types import PlayerID


class ExampleGame(IGame):
    """Example game class"""

    def __init__(self, players: list[IPlayer]) -> None:
        super().__init__(players)
        self.env: float = 0.0

    def _update(self, actions: dict[PlayerID, list[float]]) -> bool:
        for player_id, v in actions.items():
            self.env += v[0]
            self.scores[player_id] += v[0]

        return self.env > 10

    def _get_observation(self, id: PlayerID) -> list[float]:
        return [self.env]

    def _player_won(self, id: PlayerID) -> bool:
        for p, s in self.scores.items():
            if p != id and s >= self.scores[id]:
                return False
        return True

    def _validate_action(self, action) -> bool:
        if len(action) < 1:
            return False
        return int(action[0]) == action[0]

    def _player_stats(self, id: PlayerID) -> int:
        return self.scores.values()
