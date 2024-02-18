"""
This module contains the interfaces for the non-networking logic.
"""

import abc
from typing import Callable, Optional
from datetime import datetime

from comprl.shared.types import GameID, PlayerID
from comprl.server.util import IDGenerator
from comprl.server.data.interfaces import GameResult


class IAction:
    """Interface for an action"""

    pass


class IPlayer(abc.ABC):
    """Interface for a player"""

    def __init__(self) -> None:
        self.id: PlayerID = IDGenerator.generate_player_id()
        self.user_id: Optional[int] = None

    @abc.abstractmethod
    def authenticate(self, result_callback):
        """authenticates player

        Args:
            result_callback (Callable): callback
        """
        ...

    @abc.abstractmethod
    def is_ready(self, result_callback) -> bool:
        """checks if the player is ready to play

        Returns:
            bool: returns true if the player is ready to play
        """
        ...

    @abc.abstractmethod
    def notify_start(self, game_id):
        """notifies player that the game has started"""
        ...

    @abc.abstractmethod
    def get_action(self, obv, result_callback) -> IAction:
        """gets an action from the player

        Args:
            obv (Any): observation
            result_callback (Callable): callback

        Returns:
            IAction: action
        """
        ...

    @abc.abstractmethod
    def notify_end(self, result, stats):
        """notifies player that the game has ended"""
        ...

    @abc.abstractmethod
    def disconnect(self, reason: str):
        """disconnect the player"""
        ...

    @abc.abstractmethod
    def notify_error(self, error: str):
        """notifies the player of an error"""
        ...


class IGame(abc.ABC):
    """
    Interface for a game.

    Attributes:
        id (GameID):
            The unique identifier of the game.
        players (dict[PlayerID, IPlayer]):
            A dictionary of players participating in the game.
        start_time (datetime):
            The start time of the game.
        finish_callbacks (list[Callable[["IGame"], None]]):
            A list of callbacks to be executed when the game ends.
    """

    @abc.abstractmethod
    def __init__(self, players: list[IPlayer]) -> None:
        """
        Initializes a new instance of the IGame class.

        Args:
            players (list[IPlayer]): A list of players participating in the game.
        """
        self.id: GameID = IDGenerator.generate_game_id()
        self.players = {p.id: p for p in players}
        self.start_time = datetime.now()
        self.finish_callbacks: list[Callable[["IGame"], None]] = []

    def add_finish_callback(self, callback: Callable[["IGame"], None]) -> None:
        """
        Adds a callback function to be executed when the game ends.

        Args:
            callback (Callable[["IGame"], None]): The callback function to be added.
        """
        self.finish_callbacks.append(callback)

    def start(self):
        """
        Notifies all players that the game has started and starts the game cycle.
        """
        self.start_time = datetime.now()

        for player in self.players.values():
            player.notify_start(self.id)

        self._run()

    def end(self, reason="unknown"):
        """
        Notifies all players that the game has ended.

        Args:
            reason (str): The reason why the game has ended. Defaults to "unknown".
        """

        for callback in self.finish_callbacks:
            callback(self)

        for player in self.players.values():
            player.notify_end(False, 1)

    @abc.abstractmethod
    def update(self, actions: dict[PlayerID, list[float]]) -> bool:
        """
        Updates the game with the players' actions.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return False

    def _run(self):
        """
        Collects all actions and puts them in the current_actions list.
        """
        actions = {}
        for p in self.players.values():

            def _res(value, id=p.id):
                # TODO: validate action here ?
                actions[id] = value
                if len(actions) == len(self.players):
                    # all players have submitted their actions
                    # update the game, and if the game is over, end it
                    self._run() if not self.update(actions) else self.end()

            p.get_action(self.get_observation(p.id), _res)

    @abc.abstractmethod
    def _validate_action(self, action) -> bool:
        """
        Checks whether an action is valid.

        Args:
            action: The action to be validated.

        Returns:
            bool: True if the action is valid, False otherwise.
        """
        ...

    @abc.abstractmethod
    def get_observation(self, id: PlayerID) -> list[float]:
        """
        Returns the observation for the player.

        Args:
            id (PlayerID): The ID of the player for which the observation is requested.

        Returns:
            list[float]: The observation for the player.
        """
        ...

    @abc.abstractmethod
    def _player_won(self, id: PlayerID) -> bool:
        """
        Checks whether the player has won.

        Args:
            id (PlayerID): The ID of the player to be checked.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        ...

    @abc.abstractmethod
    def get_player_result(self, id: PlayerID) -> int:
        """
        Retrieves the result of a player with the given ID.

        Args:
            id (PlayerID): The ID of the player.

        Returns:
            int: The result of the player.
        """
        ...

    @abc.abstractmethod
    def get_result(self) -> GameResult:
        """
        Returns the result of the game.

        Returns:
            GameResult: The result of the game.
        """
        ...


class IServer:
    """
    Interface for the server.

    This interface defines the methods that a server implementation should provide.
    """

    @abc.abstractmethod
    def on_start(self):
        """
        Gets called when the server starts.
        """
        ...

    @abc.abstractmethod
    def on_stop(self):
        """
        Gets called when the server stops.
        """
        ...

    @abc.abstractmethod
    def on_connect(self, player: IPlayer):
        """
        Gets called when a player connects.
        Args:
            player (IPlayer): The player that has connected.
        """
        ...

    @abc.abstractmethod
    def on_disconnect(self, player: IPlayer):
        """
        Gets called when a player disconnects.
        Args:
            player (IPlayer): The player that has disconnected.
        """
        ...

    @abc.abstractmethod
    def on_update(self):
        """
        Gets called when the server updates.
        Frequency depends on the final implementation.
        """
        ...
