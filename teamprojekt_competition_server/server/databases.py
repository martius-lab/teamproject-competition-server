"""Databases"""

import sqlite3
from enum import Enum
from datetime import datetime

GAME_DB_NAME = "game"
GameEndState = Enum("GameEndState", ["WIN", "DRAW", "DISCONNECTED"])


class GameDatabase:
    """Database to store the games"""

    def __init__(self) -> None:
        self.connection = sqlite3.connect(
            "teamprojekt_competition_server/server/COMP_database.db"
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            f"""SELECT name FROM sqlite_master 
            WHERE type='table' AND name='{GAME_DB_NAME}'"""
        )
        if self.cursor.fetchone() is None:
            self.cursor.execute(
                f"""CREATE TABLE {GAME_DB_NAME}(
                    game_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    user1, 
                    user2, 
                    score1, 
                    score2,
                    start_time,
                    end_state,
                    winner,
                    disconnected)"""
            )

    def _insert_game(
        self,
        user1_id: int,
        user2_id: int,
        score_user_1: float,
        score_user_2: float,
        start_time: str,
        game_end_state: int,
        is_user1_winner=True,
        is_user1_disconnected=True,
    ) -> int | None:
        """insert a new game into the database

        Args:
            user1_id (int): user ID of user 1 (standard: winner or disconnected)
            user2_id (int): user ID of user 2 (standard: loser)
            score_user_1 (float): score of user 1
            score_user_2 (float): score of user 2
            start_time (String | None): use datetime.now().isoformat(sep=" ")
                to generate JJJJ-MM-DD HH-MM-SS.SSSS
                (example: 2024-01-14 19:23:13.736286))
            game_end_state(int): GameEndState enum value
            is_user1_winner (bool): if user 1 is the winner
                (only relevant for won games)
            is_user1_disconnected (bool): if user 1 is disconnected
                (only relevant for disconnected games)

        Returns:
            int: ID of the game
        """
        # TODO separate record file to store game steps
        if start_time is None:
            start_time = datetime.now()
            print(start_time)

        winner_id = None
        if game_end_state == GameEndState.WIN.value:
            winner_id = user1_id if is_user1_winner else user2_id

        disconnected_id = None
        if game_end_state == GameEndState.DISCONNECTED.value:
            disconnected_id = user1_id if is_user1_disconnected else user2_id

        self.cursor.execute(
            """INSERT INTO 
            game(user1, user2, score1, score2, 
            start_time, end_state, winner, disconnected) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user1_id,
                user2_id,
                score_user_1,
                score_user_2,
                start_time,
                game_end_state,
                winner_id,
                disconnected_id,
            ),
        )
        self.connection.commit()

        return self.cursor.lastrowid

    def insert_won_game(
        self,
        winner_id: int,
        loser_id: int,
        score_winner: float,
        score_loser: float,
        start_time=None,
    ) -> int | None:
        """insert a won game into the database

        Args:
            winner_id (int): user ID of the winner
            loser_id (int): user ID of the loser
            score_winner (float): score of the winner
            score_loser (float): score of the loser
            start_time (_type_, optional): use datetime module. Defaults to None.

        Returns:
            int | None: game ID
        """
        return self._insert_game(
            user1_id=winner_id,
            user2_id=loser_id,
            score_user_1=score_winner,
            score_user_2=score_loser,
            start_time=start_time,
            game_end_state=GameEndState.WIN.value,
        )

    def insert_disconnected_game(
        self,
        disconnected_user_id: int,
        other_user_id: int,
        score_disconnected_user: float,
        score_other_user: float,
        start_time=None,
    ) -> int | None:
        """insert a disconnected game into the database

        Args:
            disconnected_user_id (int): user ID of the disconnected player
            other_user_id (int): user ID of the other player
            score_disconnected_user (float): score of the disconnected player
            score_other_user (float): score of the other player
            start_time (_type_, optional): use datetime module. Defaults to None.

        Returns:
            int | None: game ID
        """
        return self._insert_game(
            user1_id=disconnected_user_id,
            user2_id=other_user_id,
            score_user_1=score_disconnected_user,
            score_user_2=score_other_user,
            start_time=start_time,
            game_end_state=GameEndState.DISCONNECTED.value,
        )

    def insert_drawn_game(
        self,
        user1_id: int,
        user2_id: int,
        score_user_1: float,
        score_user_2: float,
        start_time=None,
    ) -> int | None:
        """insert a drawn game into the database

        Args:
            user1_id (int): user ID of user 1
            user2_id (int): user ID of user 2
            score_user_1 (float): score of user 1
            score_user_2 (float): score of user 2
            start_time (_type_, optional): use datetime module. Defaults to None.

        Returns:
            int | None: game ID
        """
        return self._insert_game(
            user1_id=user1_id,
            user2_id=user2_id,
            score_user_1=score_user_1,
            score_user_2=score_user_2,
            start_time=start_time,
            game_end_state=GameEndState.DRAW.value,
        )

    def get_user_ids(self, game_id: int) -> tuple[int, int]:
        """get the IDs of the users that participated in a game

        Args:
            game_id (int): ID of the game

        Returns:
            (int, int): IDs of both users
        """
        res = self.cursor.execute(
            f"SELECT user1, user2 FROM {GAME_DB_NAME} WHERE game_ID=?", (game_id,)
        )
        users = res.fetchone()
        return users

    def get_game_ids(self, user_id: int) -> list[int]:
        """get all games that a user participated in

        Args:
            userID (int): ID of the user

        Returns:
            list[int]: IDs of the games
        """
        res = self.cursor.execute(
            f"SELECT game_ID FROM {GAME_DB_NAME} WHERE user1=? OR user2=?",
            (user_id, user_id),
        )
        games = []
        for (result,) in res.fetchall():
            games.append(result)
        return games

    def get_won_game_ids(self, user_id: int) -> list[int]:
        """get all games that a user has won

        Args:
            user_id (int): ID of the user

        Returns:
            list[int]: IDs of the games
        """
        res = self.cursor.execute(
            f"SELECT game_ID FROM {GAME_DB_NAME} WHERE winner=? AND end_state=1",
            (user_id,),
        )
        games = []
        for (result,) in res.fetchall():
            games.append(result)
        return games

    def count_played_games(self, user_id: int) -> int:
        """count all games the user has played (disconnected and drawn games included)

        Args:
            user_id (int): ID of the user

        Returns:
            int: count of played games
        """
        res = self.cursor.execute(
            f"SELECT COUNT() FROM {GAME_DB_NAME} WHERE user1=? OR user2=?",
            (user_id, user_id),
        )
        return res.fetchone()[0]

    def count_won_games(self, user_id: int) -> int:
        """count all games where the user has won

        Args:
            user_id (int): ID of the user

        Returns:
            int: count of won games
        """
        res = self.cursor.execute(
            f"SELECT COUNT() FROM {GAME_DB_NAME} WHERE winner=?",
            (user_id,),
        )
        return res.fetchone()[0]

    def count_disconnected_games(self, user_id: int) -> int:
        """count all games where the user disconnected

        Args:
            user_id (int): ID of the user

        Returns:
            int: count of disconnected games
        """
        res = self.cursor.execute(
            f"SELECT COUNT() FROM {GAME_DB_NAME} WHERE disconnected=?",
            (user_id,),
        )
        return res.fetchone()[0]

    def count_games_with_disconnect(self, user_id: int) -> int:
        """count all games where the user or the opponent disconnected

        Args:
            user_id (int): ID of the user

        Returns:
            int: count of disconnected games
        """
        res = self.cursor.execute(
            f"""SELECT COUNT() FROM {GAME_DB_NAME} 
            WHERE (user1=? OR user2=?) AND end_state=3""",
            (user_id, user_id),
        )
        return res.fetchone()[0]

    def win_rate(self, user_id: int) -> float:
        """calculates the win-rate of the user (ignoring disconnected games)

        Args:
            user_id (int): ID of the user

        Returns:
            float: win-rate
        """
        all_games = self.count_played_games(user_id)
        disconnected_games = self.count_games_with_disconnect(user_id)
        won_games = self.count_won_games(user_id)
        return won_games / (all_games - disconnected_games)
