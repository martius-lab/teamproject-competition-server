"""
Implementation of the data access objects for managing game and user data in SQLite.
"""

from __future__ import annotations

import dataclasses
import sqlite3
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


from comprl.server.data.interfaces import GameResult, UserRole
from comprl.shared.types import GameID


@dataclasses.dataclass
class SQLiteConnectionInfo:
    """
    Represents the connection information for SQLite database.

    Attributes:
        host (str): The host of the SQLite database.
        table (int): The table number in the database.
    """

    host: str
    table: str


class Base(sa.orm.MappedAsDataclass, sa.orm.DeclarativeBase):
    """Base class for all ORM classes."""


class User(Base):
    """A User."""

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    token: Mapped[str] = mapped_column(sa.String(64))
    role: Mapped[str] = mapped_column(default="user")
    mu: Mapped[float] = mapped_column(default=25.0)
    sigma: Mapped[float] = mapped_column(default=8.333)


class Game(Base):
    """Games."""

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[str] = mapped_column(unique=True)
    # TODO foreign key
    user1: Mapped[int]
    user2: Mapped[int]
    score1: Mapped[float]
    score2: Mapped[float]
    start_time: Mapped[str]
    end_state: Mapped[int]
    winner: Mapped[Optional[int]]
    disconnected: Mapped[Optional[int]]


class GameData:
    """
    Represents a data access object for managing game data in a SQLite database.

    Attributes:
        connection (sqlite3.Connection): The connection to the SQLite database.
        cursor (sqlite3.Cursor): The cursor for executing SQL queries.

    """

    def __init__(self, connection: SQLiteConnectionInfo) -> None:
        # connect to the database
        self.connection = sqlite3.connect(connection.host)
        self.cursor = self.connection.cursor()
        self.table = connection.table

        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
            game_id TEXT NOT NULL PRIMARY KEY,
            user1, 
            user2, 
            score1, 
            score2,
            start_time,
            end_state,
            winner,
            disconnected)"""
        )

    def add(self, game_result: GameResult) -> None:
        """
        Adds a game result to the database.

        Args:
            game_result (GameResult): The game result to be added.

        """
        self.cursor.execute(
            f"""INSERT INTO {self.table} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                str(game_result.game_id),
                game_result.user1_id,
                game_result.user2_id,
                game_result.score_user_1,
                game_result.score_user_2,
                game_result.start_time,
                game_result.end_state,
                game_result.winner_id,
                game_result.disconnected_id,
            ),
        )
        self.connection.commit()

    def remove(self, game_id: GameID) -> None:
        """
        Removes a game from the database based on its ID.

        Args:
            game_id (str): The ID of the game to be removed.

        """
        self.cursor.execute(
            f"""DELETE FROM {self.table} WHERE game_id=?""",
            (game_id,),
        )
        self.connection.commit()

    # TODO:  I skipped some functions here due to time constraints.
    #       And cuurently no use of them in the code...


class UserData:
    """
    Represents a data access object for managing game data in a SQLite database.

    Attributes:
        connection (sqlite3.Connection): The connection to the SQLite database.
        cursor (sqlite3.Cursor): The cursor for executing SQL queries.
    """

    def __init__(self, connection: SQLiteConnectionInfo) -> None:
        """
        Initializes a new instance of the UserData class.

        Args:
            connection (SQLiteConnectionInfo): The connection information for SQLite.
        """
        # connect to the database
        self.connection = sqlite3.connect(connection.host)
        self.cursor = self.connection.cursor()
        self.table = connection.table

        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {connection.table} (
            user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            token TEXT NOT NULL,
            mu FLOAT NOT NULL DEFAULT 25.0,
            sigma FLOAT NOT NULL DEFAULT 8.333
            )"""
        )

    def add(
        self,
        user_name: str,
        user_password: str,
        user_token: str,
        user_role=UserRole.USER,
        user_mu=25.000,
        user_sigma=8.333,
    ) -> int:
        """
        Adds a new user to the database.

        Args:
            user_name (str): The name of the user.
            user_password (str): The password of the user.
            user_token (str): The token of the user.
            user_role (UserRole, optional): The role of the user.
            Defaults to UserRole.USER.
            user_mu (float, optional): The mu value of the user. Defaults to 25.
            user_sigma (float, optional): The sigma value of the user. Defaults to 8.33.

        Returns:
            int: The ID of the newly added user.
        """

        user_role = user_role.value

        self.cursor.execute(
            f"""INSERT INTO {self.table}(username, password, role, token, mu, sigma)
            VALUES (?,?,?,?,?,?)""",
            (user_name, user_password, user_role, user_token, user_mu, user_sigma),
        )
        self.cursor.execute(
            f"""SELECT user_id FROM {self.table} WHERE token=?""",
            (user_token,),
        )
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def remove(self, user_id: int) -> None:
        """
        Removes a user from the database based on their ID.

        Args:
            user_id (int): The ID of the user to be removed.
        """
        self.cursor.execute(
            f"""DELETE FROM {self.table} WHERE user_id=?""",
            (user_id,),
        )
        self.connection.commit()

    def is_verified(self, user_token: str) -> bool:
        """
        Checks if a user is verified based on their token.

        Args:
            user_token (str): The token of the user.

        Returns:
            bool: True if the user is verified, False otherwise.
        """
        self.cursor.execute(
            f"""SELECT user_id FROM {self.table} WHERE token=?""",
            (user_token,),
        )
        result = self.cursor.fetchone()
        if result is not None:
            return True
        return False

    def get_user_id(self, user_token: str) -> int | None:
        """
        Retrieves the ID of a user based on their token.

        Args:
            user_token (str): The token of the user.

        Returns:
            int: The ID of the user, or -1 if the user is not found.
        """
        self.cursor.execute(
            f"""SELECT user_id FROM {self.table} WHERE token=?""",
            (user_token,),
        )
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]

        return None

    def get_matchmaking_parameters(self, user_id: int) -> tuple[float, float]:
        """
        Retrieves the matchmaking parameters of a user based on their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            tuple[float, float]: The mu and sigma values of the user.
        """
        self.cursor.execute(
            f"""SELECT mu, sigma FROM {self.table} WHERE user_id=?""",
            (user_id,),
        )
        return self.cursor.fetchone()

    def set_matchmaking_parameters(self, user_id: int, mu: float, sigma: float) -> None:
        """
        Sets the matchmaking parameters of a user based on their ID.

        Args:
            user_id (int): The ID of the user.
            mu (float): The new mu value of the user.
            sigma (float): The new sigma value of the user.
        """
        self.cursor.execute(
            f"""UPDATE {self.table} SET mu=?, sigma=? WHERE user_id=?""",
            (mu, sigma, user_id),
        )
        self.connection.commit()


def create_database_tables(db_path: str) -> None:
    """Create the database tables in the given SQLite database."""
    engine = sa.create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
