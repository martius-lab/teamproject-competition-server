"""Class to store the result of a game"""

from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

GameEndState = Enum("GameEndState", ["WIN", "DRAW", "DISCONNECTED"])


class GameResult:
    """Result and statistics of a game"""

    def __init__(
        self,
        game_id: UUID,
        user1_id: Optional[int],
        user2_id: Optional[int],
        score_user_1: float,
        score_user_2: float,
        start_time=None,
        end_state: int = GameEndState.WIN.value,
        is_user1_winner: bool = True,
        is_user1_disconnected: bool = True,
    ) -> None:
        """initialize a game result

        Args:
            game_id (UUID): id of the game
            user1_id (int): id of the first user
            user2_id (int): id of the second user
            score_user_1 (float): score of the first user
            score_user_2 (float): score of the second user
            start_time (str, optional): time, when the game started.
                Defaults to None (current time).
            end_state (int, optional): end-state of the game.
                Defaults to GameEndState.WIN.value.
            is_user1_winner (bool, optional): is user 1 the winner?
                Defaults to True.
            is_user1_disconnected (bool, optional): is user 1 disconnected?
                Defaults to True.
        """
        self.game_id = game_id
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.score_user_1 = score_user_1
        self.score_user_2 = score_user_2
        self.start_time = start_time
        self.end_state = end_state

        if self.start_time is None:
            self.start_time = datetime.now()

        self.winner_id = None
        if end_state == GameEndState.WIN.value:
            self.winner_id = user1_id if is_user1_winner else user2_id

        self.disconnected_id = None
        if end_state == GameEndState.DISCONNECTED.value:
            self.disconnected_id = user1_id if is_user1_disconnected else user2_id
