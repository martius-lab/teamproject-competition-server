"""
This module contains the interfaces for the game data.
"""

from datetime import datetime
from enum import IntEnum, Enum
from typing import Optional

from comprl.shared.types import GameID


class GameEndState(IntEnum):
    """
    Represents the possible end states of a game.

    Attributes:
        WIN: The game ended with a win.
        DRAW: The game ended in a draw.
        DISCONNECTED: The game ended due to a disconnection.
    """

    WIN = 0
    DRAW = 1
    DISCONNECTED = 2


class GameResult:
    """Result and statistics of a game"""

    def __init__(
        self,
        game_id: GameID,
        user1_id: int,
        user2_id: int,
        score_user_1: float,
        score_user_2: float,
        start_time: Optional[datetime] = None,
        end_state: GameEndState = GameEndState.WIN,
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
                Defaults to GameEndState.WIN.
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
        self.end_state = end_state

        if start_time is None:
            self.start_time = datetime.now()
        else:
            self.start_time = start_time

        self.winner_id = None
        if end_state == GameEndState.WIN:
            self.winner_id = user1_id if is_user1_winner else user2_id

        self.disconnected_id = None
        if end_state == GameEndState.DISCONNECTED:
            self.disconnected_id = user1_id if is_user1_disconnected else user2_id


class UserRole(Enum):
    """
    Represents the possible user roles.

    Attributes:
        USER: Normal user without administrative rights.
        ADMIN: User with administrative rights.
        BOT: Bot-user.  Bots are treated differently during matchmaking.
    """

    USER = "user"
    ADMIN = "admin"
    BOT = "bot"
