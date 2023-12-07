"""defines interfaces for the server logic"""

import logging as log

import abc

class IPlayer(abc.ABC):
    
    @abc.abstractmethod
    async def authenticate(self):
        ...
    
    @abc.abstractmethod
    async def notify_start(self):
        ...

    @abc.abstractmethod
    async def get_action(self, obv):
        ...

    @abc.abstractmethod
    async def notify_end(self):
        ...


class IGame(abc.ABC):
    """game interface"""
    
    players : list[IPlayer] = []
    
    def __init__(self, players : list[IPlayer]) -> None:
        self.players = players

    async def start(self):
        for p in self.players:
            if not await p.notify_start():
                log.error("player not ready...")

    async def end(self, reason="unknown"):
        for p in self.players:
            await p.notify_end(reason)

    @abc.abstractmethod
    async def _game_cycle(self):
        """sends a step request to both players and changes the enviroment accordingly."""
        ...
    
    @abc.abstractmethod
    async def _validate_action(self, action) -> bool:
        """check weather an action is valid"""
        ...

    @abc.abstractmethod
    async def _is_finished(self) -> bool:
        """detirmens if the game has ended

        Returns:
            bool: returns true if game has ended
        """
        ...