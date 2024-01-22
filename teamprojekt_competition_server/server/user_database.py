"""User-Database-Module"""

import sqlite3

USER_DB_NAME = "user"


# Connect to the database:
connection = sqlite3.connect("teamprojekt_competition_server/server/COMP_database.db")
cursor = connection.cursor()
cursor.execute(
    f"""
    CREATE TABLE IF NOT EXISTS {USER_DB_NAME} (
        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        token INTEGER NOT NULL,
        TS_mu FLOAT NOT NULL,
        TS_sigma FLOAT NOT NULL
    )"""
)


def _is_token_taken(new_token: int) -> bool:
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
        (new_token,),
    )
    count = cursor.fetchone()[0]
    return count > 0


def add_user(user_name: str, user_token: int, mu=25.000, sigma=8.333) -> int | None:
    """adds a new user to the database

    Args:
        user_name (str): name of the user
        user_token (int): token for the user (must be unique for every user)
        mu (float, optional): needed for TrueSkill. Defaults to 25.000.
        sigma (float, optional): needed for TrueSkill. Defaults to 8.333.

    Returns:
        int | None: returns the user_id
    """
    assert not _is_token_taken(user_token)
    cursor.execute(
        f"""
        INSERT INTO {USER_DB_NAME}(name, token, TS_mu, TS_sigma) VALUES (?,?,?,?)""",
        (user_name, user_token, mu, sigma),
    )
    connection.commit()
    return cursor.lastrowid


def get_user(id: int) -> tuple:
    """returns the database entry for the user with this id

    Args:
        id (int): the id of the user

    Returns:
        tuple: the database entry
    """
    cursor.execute(
        f"""
        SELECT * FROM {USER_DB_NAME} WHERE user_id = ?
    """,
        (id,),
    )
    user = cursor.fetchone()
    return user


def verify_user(user_token: int) -> int:
    """returns the corresponding user_id for a token

    Args:
        user_token (int): token for which the user should be found

    Returns:
        int: user_id
    """
    res = cursor.execute(
        f"""
        SELECT user_id FROM {USER_DB_NAME} WHERE token = ?
    """,
        (user_token,),
    )
    (id,) = res.fetchone()
    return id


def get_all_users() -> list[tuple]:
    """returns the database entries for all users

    Returns:
        list[tuple]: database entries of all users
    """
    cursor.execute(
        f"""
        SELECT * FROM {USER_DB_NAME}
    """
    )
    users = cursor.fetchall()
    return users


def update_user_TS(id: int, new_mu: float, new_sigma: float):
    """updates the mu and sigma entries required for TrueSkill for one user

    Args:
        id (int): user id
        new_mu (float): new mu value
        new_sigma (float): new sigma value
    """
    cursor.execute(
        f"""
        UPDATE {USER_DB_NAME} SET TS_mu=?, TS_sigma=? WHERE user_id=?
    """,
        (new_mu, new_sigma, id),
    )
    connection.commit()


def delete_user(id: int) -> None:
    """deletes a user from the database

    Args:
        id (int): user id
    """
    cursor.execute(f""" DELETE FROM {USER_DB_NAME} WHERE user_id = ? """, (id,))
    connection.commit()
