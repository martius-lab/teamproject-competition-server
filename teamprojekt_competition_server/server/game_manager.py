"""Structure which handles multiple games"""

import logging as log
from queue import Queue
from typing import Type

from .interfaces import IPlayer, IGame

_games : list[IGame] = []
_queue : Queue[IPlayer] = Queue()
_game_type : Type[IGame] = IGame

def set_game_type(T : Type[IGame]) -> None:
    _game_type = T

def enter_queue(player : IPlayer) -> None:
    _queue.put(player)
    if len(_queue) >= 2:
        game = _game_type([_queue.get(), _queue.get()])
        game.start()
        _games.append(game)