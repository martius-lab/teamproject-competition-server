from enum import Enum
from uuid import UUID

GameEndState = Enum("GameEndState", ["WIN", "DRAW", "DISCONNECTED"])

class GameResult():
    def __init__(
            self,
        game_id: UUID,
        user1_id: int,
        user2_id: int,
        score_user_1: float,
        score_user_2: float,
        start_time: str,
        game_end_state: int,
        is_user1_winner: bool = True,
        is_user1_disconnected: bool = True,
    ) -> None:
        self.game_id = game_id
        self.user1_id = user1_id
        self.user1_id = user2_id
        score_user_1 = score_user_1
        score_user_2 = score_user_2
        start_time = start_time
        game_end_state = game_end_state
        is_user1_winner = is_user1_winner
        is_user1_disconnected = is_user1_disconnected,