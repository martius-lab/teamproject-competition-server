"""User-Database-Module"""

import sqlite3
import logging as log
from uuid import UUID

USER_DB_NAME = "user"


# Connect to the database:
connection = sqlite3.connect("comprl/server/COMP_database.db")
cursor = connection.cursor()
cursor.execute(
    f"""
    CREATE TABLE IF NOT EXISTS {USER_DB_NAME} (
        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        token INTEGER NOT NULL,
        mu FLOAT NOT NULL,
        sigma FLOAT NOT NULL
    )"""
)


def _is_token_taken(new_token: UUID) -> bool:
    """tests whether a token has already been assigned to another user

    Args:
        new_token (int): the token that should be tested

    Returns:
        bool:
        returns true if token has already been assigned to another user
        returns false if the token does not yet exist
    """
    cursor.execute(
        f"""
        SELECT COUNT(*) FROM {USER_DB_NAME} WHERE token=?
    """,
        (str(new_token),),
    )
    count = cursor.fetchone()[0]
    return count > 0


def add_user(
    user_name: str, user_token: UUID, user_mu=25.000, user_sigma=8.333
) -> int | None:
    """adds a new user to the database

    Args:
        user_name (str): name of the user
        user_token (UUID): token for the user (must be unique for every user)
        user_mu (float, optional): needed for Matchmaking. Defaults to 25.000.
        user_sigma (float, optional): needed for Matchmaking. Defaults to 8.333.

    Returns:
        int | None: returns the user_id
    """
    if _is_token_taken(user_token):
        raise Exception(
            f"Tried to insert already used token {user_token} into user database"
        )

    cursor.execute(
        f"""
        INSERT INTO {USER_DB_NAME}(name, token, mu, sigma) VALUES (?,?,?,?)""",
        (user_name, str(user_token), user_mu, user_sigma),
    )
    connection.commit()
    id = cursor.lastrowid
    log.debug(
        (
            "inserted user("
            f"user_id={id}, name={user_name}, token={user_token}, "
            f"mu={user_mu}, sigma={user_sigma})"
        )
    )
    return id


def get_user(id: int) -> tuple:
    """returns the database entry for the user with this id

    Args:
        id (int): the id of the user

    Returns:
        tuple(int, string, int, float, float): database entry
        (user_id, name, token, mu, sigma)
    """
    cursor.execute(
        f"""
        SELECT * FROM {USER_DB_NAME} WHERE user_id = ?
    """,
        (id,),
    )
    user = cursor.fetchone()
    return user


def verify_user(user_token: UUID) -> int:
    """returns the corresponding user_id for a token

    Args:
        user_token (UUID): token for which the user should be found

    Returns:
        int: user_id
    """
    res = cursor.execute(
        f"""
        SELECT user_id FROM {USER_DB_NAME} WHERE token = ?
    """,
        (str(user_token),),
    )
    fetched_result = res.fetchone()
    if fetched_result is None:
        raise Exception(f"Could not verify {user_token} in the user database")
    (id,) = fetched_result
    return id


def get_all_users() -> list[tuple]:
    """returns the database entries for all users

    Returns:
        list[tuple(int, string, int, float, float)]: database entries of all users
        list[(user_id, name, token, mu, sigma)]
    """
    cursor.execute(
        f"""
        SELECT * FROM {USER_DB_NAME}
    """
    )
    users = cursor.fetchall()
    return users


def update_matchmaking_parameters(id: int, new_mu: float, new_sigma: float):
    """updates the mu and sigma entries required for Matchmaking for one user

    Args:
        id (int): user id
        new_mu (float): new mu value
        new_sigma (float): new sigma value
    """
    cursor.execute(
        f"""
        UPDATE {USER_DB_NAME} SET mu=?, sigma=? WHERE user_id=?
    """,
        (new_mu, new_sigma, id),
    )
    connection.commit()


def get_matchmaking_parameters(id: int) -> tuple[float, float]:
    """gets the mu and sigma entries required for Matchmaking of the user

    Args:
        id (int): user_id

    Returns:
        (float, float): (mu, sigma)
    """
    res = cursor.execute(
        f"""
        SELECT mu, sigma FROM {USER_DB_NAME} WHERE user_id = ?
    """,
        (id,),
    )
    parameters = res.fetchone()
    return parameters


def delete_user(id: int) -> None:
    """deletes a user from the database

    Args:
        id (int): user id
    """
    cursor.execute(f""" DELETE FROM {USER_DB_NAME} WHERE user_id = ? """, (id,))
    connection.commit()
