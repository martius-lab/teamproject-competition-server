""" script to add dummy user to the user database"""

from comprl.server.data import UserData
from comprl.server.data import ConnectionInfo
import logging
import argparse

try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:
    # tomllib was added in Python 3.11.  Older versions can use tomli
    import tomli as tomllib  # type: ignore[import-not-found, no-redef]

# run with python -m comprl.scripts.dummy_user

logging.basicConfig(level=logging.DEBUG)


def insert_users():
    """inserts four dummy user to the user database"""
    user_data.add(user_name="test1", user_token="token1")
    user_data.add(user_name="test2", user_token="token2")
    user_data.add(user_name="test3", user_token="token3")
    user_data.add(user_name="test4", user_token="token4")

    logging.info("Four dummy users have been added.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="The following arguments are supported:"
    )
    parser.add_argument("--config", type=str, help="Config file")
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

    user_db_path = args.user_db_path or (data["user_db_path"] if data else "data.db")
    user_db_name = args.user_db_name or (data["user_db_name"] if data else "users")

    user_data = UserData(ConnectionInfo(user_db_path, user_db_name))

    insert_users()
    pass
