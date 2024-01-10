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
                    game_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    player1, 
                    player2, 
                    score1, 
                    score2,
                    start_time,
                    end_state,
                    winner)"""
            )

    def insert_game(
        self,
        player1_ID: int,
        player2_ID: int,
        score_player_1: float,
        score_player_2: float,
        start_time=None,
        is_player1_winner=True,
        game_end_state=GameEndState.WIN.value,
    ) -> int | None:
        """insert a new game into the database

        Args:
            player1 (int): playerID of the winner
            player2 (int): playerID of the loser

        Returns:
            int: ID of the game
        """
        # TODO separate record file to store game steps
        if start_time is None:
            start_time = datetime.now()

        winner_ID = None
        if game_end_state == GameEndState.WIN.value:
            winner_ID = player1_ID if is_player1_winner else player2_ID

        self.cursor.execute(
            """INSERT INTO 
            game(player1, player2, score1, score2, start_time, end_state, winner) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                player1_ID,
                player2_ID,
                score_player_1,
                score_player_2,
                start_time,
                game_end_state,
                winner_ID,
            ),
        )
        self.connection.commit()

        return self.cursor.lastrowid

    def get_playerIDs(self, game_ID: int) -> tuple[int, int]:
        """get the IDs of the players that participated in a game

        Args:
            gameID (int): ID of the game

        Returns:
            (int, int): IDs of the winner and the loser
        """
        res = self.cursor.execute(
            f"SELECT player1, player2 FROM {GAME_DB_NAME} WHERE game_ID=?", (game_ID,)
        )
        players = res.fetchone()
        return players

    def get_gameIDs(self, player_ID: int) -> list[int]:
        """get all games that a player participated in

        Args:
            playerID (int): ID of the player

        Returns:
            list[int]: IDs of the games
        """
        res = self.cursor.execute(
            f"SELECT game_ID FROM {GAME_DB_NAME}  WHERE player1=? OR player2=?",
            (player_ID, player_ID),
        )
        games = []
        for (result,) in res.fetchall():
            games.append(result)
        return games

    def get_won_gameIDs(self, player_ID: int) -> list[int]:
        """get all games that a player has won

        Args:
            playerID (int): ID of the player

        Returns:
            list[int]: IDs of the games
        """
        res = self.cursor.execute(
            f"SELECT game_ID FROM {GAME_DB_NAME} WHERE winner=? AND end_state=1",
            (player_ID,),
        )
        games = []
        for (result,) in res.fetchall():
            games.append(result)
        return games
