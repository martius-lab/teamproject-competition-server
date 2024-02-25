""" script to reset the game database and the mu and sigma in the user database"""

from comprl.server.data import UserData, GameData
from comprl.server.util import ConfigProvider
import logging

# run with python -m comprl.scripts.reset

logging.basicConfig(level=logging.DEBUG)


def reset_games():
    """deletes the game table"""
    game_data = GameData(ConfigProvider.get("game_data"))

    # Drop the games table if it exists
    game_data.cursor.execute(f"DROP TABLE IF EXISTS {game_data.table}")

    game_data.connection.commit()


def reset_elo():
    """reset the elo in the user database: set mu=25.000 and sigma=8.333"""
    user_data = UserData(ConfigProvider.get("user_data"))

    # reset mu=25.000 and sigma=8.333
    default_mu = 25.000
    default_sigma = 8.333
    user_data.cursor.execute(
        f"""
    UPDATE {user_data.table} SET mu = ?, sigma = ?""",
        (default_mu, default_sigma),
    )

    user_data.connection.commit()


if __name__ == "__main__":
    reset_games()
    reset_elo()
    pass
