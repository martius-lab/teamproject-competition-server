from comprl.server.data.interfaces import GameEndState, GameResult
from comprl.server.interfaces import IGame, IPlayer


class ExampleGame(IGame):
    """example for a game"""

    def __init__(self, players: list[IPlayer]) -> None:
        super().__init__(players=players)
        self.env = 0

    def _update_environment(self):
        self.env += sum(sum(self.current_actions, []))

    def _validate_action(self, action):
        return isinstance(action, int)

    def _is_finished(self) -> bool:
        return self.env > 10

    def _observation(self, index: int = 0) -> list[float]:
        return [float(self.env)]

    def _player_stats(self, index) -> int:
        return 0

    def _player_won(self, index) -> bool:
        if index == 0:
            return True
        return False
    
    def get_result(self) -> GameResult:
        return GameResult(self.id, -1, -1, 0,0, None, GameEndState.DRAW, True, True)
