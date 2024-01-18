"""User-Database-Module"""

import sqlite3

USER_DB_NAME = "user"


# Connect to the database:
connection = sqlite3.connect('teamprojekt_competition_server/server/COMP_database.db')
cursor = connection.cursor()
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {USER_DB_NAME} (
        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        token INTEGER NOT NULL,
        TS_mu FLOAT NOT NULL,
        TS_sigma FLOAT NOT NULL
    )""")

def _is_token_taken(new_token: int) -> bool:
    cursor.execute(f"""
        SELECT COUNT(*) FROM {USER_DB_NAME} WHERE token=?
    """, (new_token,))
    count = cursor.fetchone()[0]
    return count > 0


def add_user(
        user_name: str, user_token: int, mu=25.000, sigma = 8.333 
) -> int | None:
    assert not _is_token_taken(user_token)
    cursor.execute(f"""
                   INSERT INTO {USER_DB_NAME}(name, token, TS_mu, TS_sigma) VALUES (?,?,?,?)""", (user_name, user_token, mu, sigma))
    connection.commit()
    return cursor.lastrowid



def get_user(id: int) -> tuple:
    cursor.execute(f"""
        SELECT * FROM {USER_DB_NAME} WHERE user_id = ?
    """, (id,))
    user = cursor.fetchone()
    return user


def get_all_users() -> list[tuple]:
    cursor.execute(f"""
        SELECT * FROM {USER_DB_NAME}
    """)
    users = cursor.fetchall()
    return users


def update_user_TS(id: int, new_mu:float, new_sigma:float):
    cursor.execute(f"""
        UPDATE {USER_DB_NAME} SET TS_mu=?, TS_sigma=? WHERE user_id=?
    """, (new_mu, new_sigma, id))
    connection.commit()


def delete_user(id: int) -> None:
    cursor.execute(f""" DELETE FROM {USER_DB_NAME} WHERE user_id = ? """, (id,))
    connection.commit()

