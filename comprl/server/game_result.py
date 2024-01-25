import datetime
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
        self.user2_id = user2_id
        self.score_user_1 = score_user_1
        self.score_user_2 = score_user_2
        self.start_time = start_time
        self.game_end_state = game_end_state

        if self.start_time is None:
            self.start_time = datetime.now()

        self.winner_id = None
        if game_end_state == GameEndState.WIN.value:
            self.winner_id = user1_id if is_user1_winner else user2_id

        self.disconnected_id = None
        if game_end_state == GameEndState.DISCONNECTED.value:
            self.disconnected_id = user1_id if is_user1_disconnected else user2_id