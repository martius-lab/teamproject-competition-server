""" script to reset the game database and the mu and sigma in the user database"""

import sqlite3
import logging

# run with python -m comprl.scripts.reset

logging.basicConfig(level=logging.DEBUG)


def reset_games():
    """deletes the game table"""
    GAME_DB_NAME = "game"
    GAME_DB_FILE = "comprl/server/COMP_database.db"

    # Connect to the database:
    connection = sqlite3.connect(GAME_DB_FILE)
    cursor = connection.cursor()

    # Drop the games table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS {GAME_DB_NAME}")

    connection.commit()
    connection.close()


def reset_elo():
    """reset the elo in the user database: set mu=25.000 and sigma=8.333"""
    USER_DB_NAME = "user"
    USER_DB_FILE = "comprl/server/COMP_database.db"

    # Connect to the database:
    connection = sqlite3.connect(USER_DB_FILE)
    cursor = connection.cursor()

    # reset mu=25.000 and sigma=8.333
    default_mu = 25.000
    default_sigma = 8.333
    cursor.execute(
        f"""
    UPDATE {USER_DB_NAME} SET mu = ?, sigma = ?""",
        (default_mu, default_sigma),
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    reset_games()
    reset_elo()
    pass
