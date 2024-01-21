"""Structure which handles multiple games"""

import logging as log
from typing import Type

from .interfaces import IGame
from ..shared.types import GameID, PlayerID

from . import player_manager

_running_games: dict[GameID, IGame] = {}

# FIXME how to do this better?
_game_type: Type[IGame] = IGame  # type: ignore[type-abstract]


def set_game_type(T: Type[IGame]) -> None:
    """set the game class for the current running instance

    Args:
        T (Type[IGame]): type of the class we want to use
    """
    global _game_type
    _game_type = T


def start_game(player_ids: list[PlayerID]) -> None:
    """start a game with the given id's

    Args:
        player_ids (list[PlayerID]): id's of the players we wan't to play with
    """
    players = [player_manager.get_player_by_id(id) for id in player_ids]

    # we maybe get a invalid ID here, better to not start the game
    if None in players:
        log.error("Tried starting a game with at least on invalid PlayerID")
        return

    game = _game_type([player for player in players if player is not None])
    game.start()
    game.add_finish_callback(_game_ended)

    _running_games[game.id] = game


def _game_ended(id: GameID):
    """get's called if a running game ends

    Args:
        id (GameID): id of the ended game
    """
    if id not in _running_games:
        log.error("Stopping non registered game!")
        return

    game = _running_games.pop(id)
