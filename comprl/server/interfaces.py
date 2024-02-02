"""
This module contains the interfaces for the non-networking logic.
"""

import abc
from typing import Callable
from datetime import datetime

from comprl.shared.types import GameID, PlayerID
from comprl.server import util
from comprl.server.data.interfaces import GameResult

class IAction:
    """Interface for an action"""

    pass


class IPlayer(abc.ABC):
    """Interface for a player"""

    def __init__(self) -> None:
        self.id: PlayerID = util.IDGenerator.generate_player_id()

    @abc.abstractmethod
    def authenticate(self, result_callback):
        """authenticates player

        Args:
            result_callback (Callable): callback
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
    """game interface"""

    def __init__(self, players: list[IPlayer]) -> None:
        self.players: list[IPlayer] = players
        self.current_actions: list = [None for _ in players]
        self.result_received: int = 0
        self.id: GameID = util.IDGenerator.generate_game_id()
        self.start_time = None

        self.finish_callbacks: list[Callable] = []

    def add_finish_callback(self, callback: Callable) -> None:
        """link a callback to the end of a game"""
        self.finish_callbacks.append(callback)

    def start(self):
        """
        notifies all players that the game has started
        and starts the game cycle
        """

        self.start_time = datetime.now()

        for p in self.players:
            p.notify_start(game_id=self.id)

        self._game_cycle()

    def end(self, reason="unknown"):
        """notifies all players that the game has ended

        Args:
            reason (str, optional): reason why the game has ended. Defaults to "unknown"
        """
        for c in self.finish_callbacks:
            c(self.id)

    @abc.abstractmethod
    def _update_environment(self):
        """works with the current_actions list to change the environment accordingly."""
        ...

    def _game_cycle(self):
        """collects all actions and puts them in current_actions list"""
        self.result_received = 0

        for i, p in enumerate(self.players):

            def __res(v: IAction, index=i):
                # log.debug(f"got action {v} from player {index}")
                # TODO: add validation here!
                self.current_actions[index] = v
                self.result_received += 1
                if self.result_received == len(self.players):
                    self._update_environment()

                    if self._is_finished():
                        self.end()
                    else:
                        self._game_cycle()

            p.get_action(obv=self._observation(index=i), result_callback=__res)

    @abc.abstractmethod
    def _validate_action(self, action) -> bool:
        """check weather an action is valid"""
        ...

    @abc.abstractmethod
    def _is_finished(self) -> bool:
        """determines if the game has ended

        Returns:
            bool: returns true if game has ended
        """
        ...

    @abc.abstractmethod
    def _observation(self, index: int = 0) -> list[float]:
        """returns the observation for the player"""
        ...

    @abc.abstractmethod
    def _player_won(self, index) -> bool:
        """check wether the player has won

        Returns:
            bool: returns true if player has won
        """
        ...

    @abc.abstractmethod
    def _player_stats(self, index) -> int:
        """returns the player stats"""
        ...

    @abc.abstractmethod
    def get_result(self) -> GameResult:
        """returns the result and the statistics of the game"""
        ...


class IServer:
    """Interface for the server"""

    @abc.abstractmethod
    def on_start(self):
        """Runs the server"""
        ...

    @abc.abstractmethod
    def on_stop(self):
        """Stops the server"""
        ...

    @abc.abstractmethod
    def on_connect(self, player: IPlayer):
        """Connects a player to the server"""
        ...

    @abc.abstractmethod
    def on_disconnect(self, player: IPlayer):
        """Disconnects a player from the server"""
        ...

    @abc.abstractmethod
    def on_update(self):
        """
        Updates the server, called every tick (depends on the server implementation)
        """
        ...
