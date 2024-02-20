from comprl.server.data.interfaces import GameEndState, GameResult
from comprl.server.interfaces import IGame, IPlayer
from comprl.shared.types import PlayerID


class ExampleGame(IGame):
    """Example game class"""

    def __init__(self, players: list[IPlayer]) -> None:
        super().__init__(players)
        self.env: float = 0.0

    def update(self, actions: dict[PlayerID, list[float]]) -> bool:
        for _, v in actions.items():
            self.env += v[0]

        if self.env > 10:
            return True
        return False

    def get_observation(self, id: PlayerID) -> list[float]:
        return [self.env]

    def get_result(self) -> GameResult:
        # still dunno about this generally lol
        return GameResult(
            self.id,
            list(self.players.values())[0].user_id or -1,
            list(self.players.values())[1].user_id or -1,
            0.0,
            0.0,
            self.start_time,
            GameEndState.WIN,
        )

    def _player_won(self, id: PlayerID) -> bool:
        return False

    def _validate_action(self, action) -> bool:
        return True

    def get_player_result(self, id: PlayerID) -> int:
        return 0
