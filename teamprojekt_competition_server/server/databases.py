"""Databases"""

import sqlite3

GAME_DB_NAME = "game"


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
            self.cursor.execute(f"CREATE TABLE {GAME_DB_NAME}(winnerID, loserID)")

    def insert_game(self, winnerID: int, loserID: int) -> int | None:
        """insert a new game into the database

        Args:
            winnerID (int): playerID of the winner
            loserID (int): playerID of the loser

        Returns:
            int: ID of the game
        """
        # TODO separate record file to store game steps
        self.cursor.execute(f"INSERT INTO game VALUES ({winnerID}, {loserID})")
        self.connection.commit()
        return self.cursor.lastrowid

    def get_playerIDs(self, gameID: int) -> tuple[int, int]:
        """get the IDs of the players that participated in a game

        Args:
            gameID (int): ID of the game

        Returns:
            (int, int): IDs of the winner and the loser
        """
        res = self.cursor.execute(
            f"SELECT winnerID, loserID FROM {GAME_DB_NAME} WHERE rowid={gameID}"
        )
        players = res.fetchone()
        return players

    def get_gameIDs(self, playerID: int) -> list[int]:
        """get all games that a player participated in

        Args:
            playerID (int): ID of the player

        Returns:
            list[int]: IDs of the games
        """
        res = self.cursor.execute(
            f"""SELECT rowid FROM {GAME_DB_NAME}  
            WHERE winnerID={playerID} OR loserID={playerID}"""
        )
        games = []
        for (result,) in res.fetchall():
            games.append(result)
        return games

    def get_won_gameIDs(self, playerID: int) -> list[int]:
        """get all games that a player has won

        Args:
            playerID (int): ID of the player

        Returns:
            list[int]: IDs of the games
        """
        res = self.cursor.execute(
            f"SELECT rowid FROM {GAME_DB_NAME} WHERE winnerID={playerID}"
        )
        games = []
        for (result,) in res.fetchall():
            games.append(result)
        return games
