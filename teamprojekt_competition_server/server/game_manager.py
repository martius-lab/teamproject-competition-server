"""Structure which handles multiple games"""

import logging as log
from typing import Type

from .interfaces import IGame
from ..shared.types import GameID, PlayerID

_running_games : dict[GameID, IGame] = []
_game_type : Type[IGame] = IGame

def set_game_type(T : Type[IGame]) -> None:
    _game_type = T
    
def start_game(players : list[PlayerID]) -> None:
    game = _game_type(players)
    game.start()
    game.add_finish_callback(_game_ended)
    _running_games[game.id] = game
    
def _game_ended(id : PlayerID):
    if id not in _running_games:
        log.error("Stopping non registered game!")
        return

    game = _running_games.pop(PlayerID)