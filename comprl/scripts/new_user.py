""" script to add new user to the user database"""
import comprl.server.user_database as user_db
import logging
import uuid

# run with python -m comprl.scripts.new_user

logging.basicConfig(level=logging.DEBUG)


def insert_user(name: str):
    """inserts a user to the user_db with a random token and a given name

    Args:
        name (str): name of the new user
    """
    user_db.add_user(user_name=name, user_token=uuid.uuid4())


if __name__ == "__main__":
    while True:
        name = input(
            "Please enter a name for the user or press ENTER to end the script: "
        )
        if name:
            insert_user(name)
        else:
            break
    pass
