""" script to add new user to the user database"""

from comprl.server.data import UserData
from comprl.server.util import ConfigProvider
import logging
import random
import string

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
    name = input("Please enter a name for the user or press ENTER to end the script: ")
    while name:
        insert_user(name)
        name = input(
            "Please enter a name for the user or press ENTER to end the script: "
        )
    pass
