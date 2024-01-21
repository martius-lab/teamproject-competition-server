import logging as log
from typing import Optional
import uuid

from .interfaces import IPlayer, PlayerID

from . import matchmaking

_connected_players: dict[PlayerID, IPlayer] = {}
_authenticated_players: dict[PlayerID, bool] = {}


def register(player: IPlayer) -> None:
    """register a player that connected to the server

    Args:
        player (IPlayer): player to register
    """
    _connected_players[player.id] = player
    log.debug(f"Player registered with id:{player.id}")


def authenticate(id: PlayerID, token: str) -> None:
    """authenticates a registered player

    Args:
        id (PlayerID): id of the player to authenticate
        token (str): autheticaten token
    """
    log.debug(f"Player authenticated with id:{id} authenticated with token:{token}")

    if id in _connected_players:
        _authenticated_players[id] = True
        matchmaking.match(id)


def remove(id: PlayerID) -> None:
    """remove player from the manager

    Args:
        id (PlayerID): id to remove
    """
    if id in _connected_players:
        log.debug(f"Player with id:{id} disconnected")
        del _connected_players[id]

    if id in _authenticated_players:
        del _authenticated_players[id]


def get_player_by_id(id: PlayerID) -> Optional[IPlayer]:
    """get the obejct of a authenticated player

    Args:
        id (PlayerID): id of the player

    Returns:
        Optional[IPlayer]: contains the IPlayer object if authenticated
    """
    if id in _authenticated_players:
        return _connected_players[id]

    log.error("Tried acsess of not authenticated player!")
    return None
