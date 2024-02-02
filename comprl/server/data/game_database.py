"""Database to store the games"""

import sqlite3
import logging as log
from uuid import UUID

from .game_result import GameResult

GAME_DB_NAME = "game"
GAME_DB_FILE = "comprl/server/COMP_database.db"

# Connect to the database:
connection = sqlite3.connect(GAME_DB_FILE)
cursor = connection.cursor()
cursor.execute(
    f"""SELECT name FROM sqlite_master 
    WHERE type='table' AND name='{GAME_DB_NAME}'"""
)
if cursor.fetchone() is None:
    cursor.execute(
        f"""CREATE TABLE {GAME_DB_NAME}(
            game_id TEXT NOT NULL PRIMARY KEY,
            user1, 
            user2, 
            score1, 
            score2,
            start_time,
            end_state,
            winner,
            disconnected)"""
    )


def insert_game(game_result: GameResult):
    """inserts a game into the database

    Args:
        game_result (GameResult): results and statistics of the game

    """
    # TODO separate record file to store game steps

    cursor.execute(
        """INSERT INTO 
        game VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            str(game_result.game_id),
            game_result.user1_id,
            game_result.user2_id,
            game_result.score_user_1,
            game_result.score_user_2,
            game_result.start_time,
            game_result.end_state,
            game_result.winner_id,
            game_result.disconnected_id,
        ),
    )
    connection.commit()
    log.debug(
        (
            "inserted game("
            f"game_id={game_result.game_id}, "
            f"user1={game_result.user1_id}, user2={game_result.user2_id}, "
            f"score1={game_result.score_user_1}, score2={game_result.score_user_2}, "
            f"start_time={game_result.start_time}, "
            f"end_state={game_result.end_state}, "
            f"winner={game_result.winner_id}, "
            f"disconnected={game_result.disconnected_id})"
        )
    )


def get_user_ids(game_id: UUID) -> tuple[int, int]:
    """get the IDs of the users that participated in a game

    Args:
        game_id (int): ID of the game

    Returns:
        (int, int): IDs of both users
    """
    res = cursor.execute(
        f"SELECT user1, user2 FROM {GAME_DB_NAME} WHERE game_ID=?", (str(game_id),)
    )
    users = res.fetchone()
    return users


def get_game_ids(user_id: int) -> list[UUID]:
    """get all games that a user participated in

    Args:
        userID (int): ID of the user

    Returns:
        list[int]: IDs of the games
    """
    res = cursor.execute(
        f"SELECT game_ID FROM {GAME_DB_NAME} WHERE user1=? OR user2=?",
        (user_id, user_id),
    )
    games = []
    for (result,) in res.fetchall():
        games.append(UUID(result))
    return games


def get_won_game_ids(user_id: int) -> list[UUID]:
    """get all games that a user has won

    Args:
        user_id (int): ID of the user

    Returns:
        list[int]: IDs of the games
    """
    res = cursor.execute(
        f"SELECT game_ID FROM {GAME_DB_NAME} WHERE winner=?",
        (user_id,),
    )
    games = []
    for (result,) in res.fetchall():
        games.append(UUID(result))
    return games


def count_played_games(user_id: int) -> int:
    """count all games the user has played (disconnected and drawn games included)

    Args:
        user_id (int): ID of the user

    Returns:
        int: count of played games
    """
    res = cursor.execute(
        f"SELECT COUNT() FROM {GAME_DB_NAME} WHERE user1=? OR user2=?",
        (user_id, user_id),
    )
    return res.fetchone()[0]


def count_won_games(user_id: int) -> int:
    """count all games where the user has won

    Args:
        user_id (int): ID of the user

    Returns:
        int: count of won games
    """
    res = cursor.execute(
        f"SELECT COUNT() FROM {GAME_DB_NAME} WHERE winner=?",
        (user_id,),
    )
    return res.fetchone()[0]


def count_disconnected_games(user_id: int) -> int:
    """count all games where the user disconnected

    Args:
        user_id (int): ID of the user

    Returns:
        int: count of disconnected games
    """
    res = cursor.execute(
        f"SELECT COUNT() FROM {GAME_DB_NAME} WHERE disconnected=?",
        (user_id,),
    )
    return res.fetchone()[0]


def count_games_with_disconnect(user_id: int) -> int:
    """count all games where the user or the opponent disconnected

    Args:
        user_id (int): ID of the user

    Returns:
        int: count of disconnected games
    """
    res = cursor.execute(
        f"""SELECT COUNT() FROM {GAME_DB_NAME} 
        WHERE (user1=? OR user2=?) AND end_state=3""",
        (user_id, user_id),
    )
    return res.fetchone()[0]


def win_rate(user_id: int) -> float:
    """calculates the win-rate of the user (ignoring disconnected games)

    Args:
        user_id (int): ID of the user

    Returns:
        float: win-rate
    """
    all_games = count_played_games(user_id)
    disconnected_games = count_games_with_disconnect(user_id)
    won_games = count_won_games(user_id)
    return won_games / (all_games - disconnected_games)
