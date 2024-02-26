""" script to add new user to the user database"""

from comprl.server.data import UserData
from comprl.server.util import ConfigProvider
from comprl.server.data import ConnectionInfo
import logging
import random
import string
import argparse

try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:
    # tomllib was added in Python 3.11.  Older versions can use tomli
    import tomli as tomllib  # type: ignore[import-not-found, no-redef]

# run with python -m comprl.scripts.new_user

logging.basicConfig(level=logging.DEBUG)


def generate_random_string(length=10):
    """Generate a random string of a specified length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def insert_user(name: str):
    """inserts a user to the user_db with a random token and a given name

    Args:
        name (str): name of the new user
    """
    user_data = UserData(ConfigProvider.get("user_data"))
    token = generate_random_string()
    user_data.add(user_name=name, user_token=token)


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

    ConfigProvider.set("user_data", ConnectionInfo(user_db_path, user_db_name))

    name = input("Please enter a name for the user or press ENTER to end the script: ")
    while name:
        insert_user(name)
        name = input(
            "Please enter a name for the user or press ENTER to end the script: "
        )
    pass
