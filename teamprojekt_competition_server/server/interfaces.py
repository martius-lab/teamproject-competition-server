"""defines interfaces for the server logic"""

import logging as log

import abc


class IAction:
    pass


class IPlayer(abc.ABC):
    
    id : int = -1
    
    @abc.abstractmethod
    def authenticate(self, result_callback):
        ...

    @abc.abstractmethod
    def notify_start(self):
        ...

    @abc.abstractmethod
    def get_action(self, obv, result_callback) -> IAction:
        ...

    @abc.abstractmethod
    def notify_end(self):
        ...


class IGame(abc.ABC):
    """game interface"""

    players: list[IPlayer] = []
    current_actions: list[IAction] = []
    result_received: int = 0

    def __init__(self, players: list[IPlayer]) -> None:
        self.players = players

    def start(self):
        for p in self.players:
            p.notify_start()

    def end(self, reason="unknown"):
        for p in self.players:
            p.notify_end(reason)

    @abc.abstractmethod
    def _game_cycle(self):
        """sends a step request to both players and changes the enviroment accordingly."""

    def _request_actions(self):
        self.result_received = 0

        for i, p in enumerate(self.players):

            def __res(v: IAction):
                self.current_actions[i] = v
                self.result_received += 1
                if self.result_received == len(self.players):
                    self._game_cycle()

                    if self._is_finished():
                        self.end()
                    else:
                        self._request_actions()

            p.get_action(callback=__res)

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
