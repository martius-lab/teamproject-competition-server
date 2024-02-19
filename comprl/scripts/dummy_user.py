""" script to add dummy user to the user database"""

import comprl.server.user_database as user_db
import logging

# run with python -m comprl.scripts.dummy_user

logging.basicConfig(level=logging.DEBUG)


def insert_users():
    """inserts four dummy user to the user_db"""
    user_db.add_user(user_name="test1", user_token="token1")
    user_db.add_user(user_name="test2", user_token="token2")
    user_db.add_user(user_name="test3", user_token="token3")
    user_db.add_user(user_name="test4", user_token="token4")


if __name__ == "__main__":
    insert_users()
    pass
