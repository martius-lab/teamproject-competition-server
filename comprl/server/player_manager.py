"""manages players connection to the server"""

import logging as log
from typing import Optional

from .interfaces import IPlayer, PlayerID

from . import matchmaking
from . import user_database

_connected_players: dict[PlayerID, IPlayer] = {}
_authenticated_players: dict[PlayerID, int] = {}


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
        token (str): authenticate token
    """
    user_id = user_database.verify_user(user_token=token)

    if id not in _connected_players:
        return

    if user_id is None:
        log.debug(
            f"Player with id {id} " f"tried to authenticate with unknown token: {token}"
        )
        _connected_players[id].disconnect(
            reason="Authentication with the provided token failed"
        )
        remove(id)
    else:
        log.debug(f"Player authenticated with id:{id} authenticated with token:{token}")

        if id in _connected_players:
            _authenticated_players[id] = user_id
            matchmaking.match(id, user_id)


def match_player_by_id(player_id: PlayerID) -> None:
    """add player to matchmaking"""
    matchmaking.match(player_id, _authenticated_players[player_id])


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
    """get the object of a authenticated player

    Args:
        id (PlayerID): id of the player

    Returns:
        Optional[IPlayer]: contains the IPlayer object if authenticated
    """
    if id in _authenticated_players:
        return _connected_players[id]

    log.error("Tried access of not authenticated player!")
    return None


def get_user_id(id: PlayerID) -> Optional[int]:
    """get the object of a authenticated player

    Args:
        id (PlayerID): id of the player

    Returns:
        Optional[IPlayer]: contains the IPlayer object if authenticated
    """
    if id in _authenticated_players:
        return _authenticated_players[id]

    log.error("Tried access of not authenticated player!")
    return None
