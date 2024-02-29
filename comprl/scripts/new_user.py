""" script to add new user to the user database"""

from comprl.server.data import UserData
from comprl.server.data import ConnectionInfo
import logging
import argparse
import uuid

try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:
    # tomllib was added in Python 3.11.  Older versions can use tomli
    import tomli as tomllib  # type: ignore[import-not-found, no-redef]

# run with python -m comprl.scripts.new_user

logging.basicConfig(level=logging.DEBUG)


def insert_user(name: str):
    """inserts a user to the user_db with a random token and a given name

    Args:
        name (str): name of the new user
    """
    token = str(uuid.uuid4())
    user_data.add(user_name=name, user_password=str(uuid.uuid4()), user_token=token)


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

    name = input("Please enter a name for the user or press ENTER to end the script: ")
    while name:
        insert_user(name)
        name = input(
            "Please enter a name for the user or press ENTER to end the script: "
        )
    pass
