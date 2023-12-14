"""defines interfaces for the server logic"""

import logging as log

import abc


class IAction:
    """Interface for an action"""

    pass


class IPlayer(abc.ABC):
    """Interface for a player"""

    def __init__(self) -> None:
        self.id: int = -1

    @abc.abstractmethod
    def authenticate(self, result_callback):
        """authenticates player

        Args:
            result_callback (Callable): callback
        """
        ...

    @abc.abstractmethod
    def notify_start(self):
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


class IGame(abc.ABC):
    """game interface"""

    def __init__(self, players: list[IPlayer]) -> None:
        self.players: list[IPlayer] = players
        self.current_actions: list = [None for _ in players]
        self.result_received: int = 0

    def start(self):
        """
        notifies all players that the game has started
        and starts the game cycle
        """
        for p in self.players:
            p.notify_start()
        self._game_cycle()

    def end(self, reason="unknown"):
        """notifies all players that the game has ended

        Args:
            reason (str, optional): reason why the game has ended. Defaults to "unknown"
        """
        for i, p in enumerate(self.players):
            p.notify_end(result=self._player_won(i), stats=self._player_stats(i))

    @abc.abstractmethod
    def _update_environment(self):
        """works with the current_actions list to change the enviroment accordingly."""
        ...

    def _game_cycle(self):
        """collectes all actions and puts them in current_actions list"""
        self.result_received = 0

        for i, p in enumerate(self.players):

            def __res(v: IAction, index=i):
                log.debug(f"got action {v} from player {index}")
                self.current_actions[index] = v
                self.result_received += 1
                if self.result_received == len(self.players):
                    self._update_environment()

                    if self._is_finished():
                        self.end()
                    else:
                        self._game_cycle()

            p.get_action(obv=self._observation(), result_callback=__res)

    @abc.abstractmethod
    def _validate_action(self, action) -> bool:
        """check weather an action is valid"""
        ...

    @abc.abstractmethod
    def _is_finished(self) -> bool:
        """detirmens if the game has ended

        Returns:
            bool: returns true if game has ended
        """
        ...

    @abc.abstractmethod
    def _observation(self):
        """retutns the observation for the players"""
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
        """retutns the player stats"""
        ...
