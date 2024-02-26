""" script to reset the game database and the mu and sigma in the user database"""

from comprl.server.data import UserData, GameData
from comprl.server.data import ConnectionInfo
import logging
import argparse

try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:
    # tomllib was added in Python 3.11.  Older versions can use tomli
    import tomli as tomllib  # type: ignore[import-not-found, no-redef]

# run with python -m comprl.scripts.reset

logging.basicConfig(level=logging.DEBUG)


def reset_games(game_data: GameData):
    """deletes the game table"""

    # Drop the games table if it exists
    game_data.cursor.execute(f"DROP TABLE IF EXISTS {game_data.table}")

    game_data.connection.commit()
    logging.info("The games table has been deleted.")


def reset_elo(user_data: UserData):
    """reset the elo in the user database: set mu=25.000 and sigma=8.333"""

    # reset mu=25.000 and sigma=8.333
    default_mu = 25.000
    default_sigma = 8.333
    user_data.cursor.execute(
        f"""
    UPDATE {user_data.table} SET mu = ?, sigma = ?""",
        (default_mu, default_sigma),
    )

    user_data.connection.commit()
    logging.info(
        "The matchmaking parameters have been reset to mu=25.000 and sigma=8.333 for all users."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="The following arguments are supported:"
    )
    parser.add_argument("--config", type=str, help="Config file")
    parser.add_argument(
        "--game_db_path",
        type=str,
        help="Path to the database file (doesn't have to exist)",
    )
    parser.add_argument(
        "--game_db_name", type=str, help="Name of the game table in the file"
    )
    parser.add_argument("--user_db_path", type=str, help="Path to the database file")
    parser.add_argument(
        "--user_db_name", type=str, help="Name of the user table in the file"
    )
    args = parser.parse_args()

    data = None
    if args.config is not None:
        # load config file
        with open(args.config, "rb") as f:
            data = tomllib.load(f)["CompetitionServer"]
    else:
        print("No config file provided, using arguments or defaults")

    game_db_path = args.game_db_path or (data["game_db_path"] if data else "data.db")
    game_db_name = args.game_db_name or (data["game_db_name"] if data else "games")
    user_db_path = args.user_db_path or (data["user_db_path"] if data else "data.db")
    user_db_name = args.user_db_name or (data["user_db_name"] if data else "users")

    game_data = GameData(ConnectionInfo(game_db_path, game_db_name))
    user_data = UserData(ConnectionInfo(user_db_path, user_db_name))

    reset_games(game_data)
    reset_elo(user_data)
    pass
