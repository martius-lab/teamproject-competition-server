"""Script to add new user to the user database."""

from comprl.server.data import UserData
from comprl.server.data.interfaces import UserRole
import logging
import argparse
import uuid
import getpass

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
    password = getpass.getpass("Please enter a password for the user: ")
    isAdmin = input("Do you want the new user to be an admin? (Y/N): ")
    if isAdmin.lower() == "y":
        role = UserRole.ADMIN
    else:
        role = UserRole.USER
    user_data.add(
        user_name=name, user_password=password, user_token=token, user_role=role
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="The following arguments are supported:"
    )
    parser.add_argument("--config", type=str, help="Config file")
    parser.add_argument("--database-path", type=str, help="Path to the database file")
    args = parser.parse_args()

    data = None
    if args.config is not None:
        # load config file
        with open(args.config, "rb") as f:
            data = tomllib.load(f)["CompetitionServer"]

    if args.database_path:
        database_path = args.database_path
    elif data:
        database_path = data["database_path"]
    else:
        parser.error("Need to provide either --config or --database-path")

    user_data = UserData(database_path)

    name = input("Please enter a name for the user or press ENTER to end the script: ")
    while name:
        insert_user(name)
        name = input(
            "Please enter a name for the user or press ENTER to end the script: "
        )
