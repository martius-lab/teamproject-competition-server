"""defines interfaces for the server logic"""

import abc
from typing import Callable
from datetime import datetime

import gymnasium as gym

from comprl.shared.types import GameID, PlayerID
from comprl.server import util
from .game_result import GameResult

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

        # we might want to move this
        for i, p in enumerate(self.players):
            p.notify_end(result=self._player_won(i), stats=self._player_stats(i))

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
    def _observation(self, index: int = 0):
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
    def get_results(self) -> GameResult:
        """returns the result and the statistics of the game"""
        ...


class GymGame(IGame):
    """game class with the game logic being a gym env"""

    def __init__(
        self, players: list[IPlayer], game_id: int, env_name: str = "Pendulum-v1"
    ) -> None:
        """create a game

        Args:
            players (list[IPlayer]): list of players participating in this game.
                                      Handled by the abstract class
            env_name (str, optional): Name of the used gym env. Defaults to
                                      "Pendulum-v1" for testing purposes.
                                      The default might change later.
        """
        self.env = gym.make(
            env_name, render_mode="human"
        )  # add ', render_mode="human" ' to render the env.

        # initialize terminated and truncated, so the game hasn't ended by default.
        self.terminated = False
        self.truncated = False
        self.cycle_count = 0
        self.MAX_CYCLE_COUNT = 1000

        self.observation, self.info = self.env.reset()

        super().__init__(players)

    def start(self):
        """
        notifies all players that the game has started
        and starts the game cycle
        """
        return super().start()

    def end(self, reason="unknown"):
        """notifies all players that the game has ended

        Args:
            reason (str, optional): reason why the game has ended.
                                    Defaults to "unknown"
        """
        self.env.close()
        return super().end(reason)

    def _update_environment(self):
        """perform one gym step, using the actions collected by _game_cycle"""
        (
            self.observation,
            self.reward,
            self.terminated,
            self.truncated,
            self.info,
        ) = self.env.step(self.current_actions[1])
        self.cycle_count += 1
        if self.cycle_count > self.MAX_CYCLE_COUNT:
            self.terminated = True

    def _game_cycle(self):
        return super()._game_cycle()

    def _validate_action(self, action) -> bool:
        return self.env.action_space.contains(
            action
        )  # check if the action is in the action space and thus valid

    def _is_finished(self) -> bool:
        return self.terminated or self.truncated

    def _observation(self):
        return self.observation.tolist()  # obs is an np array, we need list

    def _player_won(self, index) -> bool:
        return False  # TODO find the winner

    def _player_stats(self, index) -> int:
        return 0  # TODO


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
