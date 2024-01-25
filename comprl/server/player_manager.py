"""manages players connection to the server"""

import logging as log
from typing import Optional
from uuid import UUID

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
    try:
        converted_token = UUID(token)
        user_id = user_database.verify_user(user_token=converted_token)
        log.debug(f"Player authenticated with id:{id} authenticated with token:{token}")

        if id in _connected_players:
            _authenticated_players[id] = user_id
            matchmaking.match(id)
    except Exception:
        log.debug(
            f"Player with id {id} " f"tried to authenticate with unknown token: {token}"
        )
        if id in _connected_players:
            _connected_players[id].disconnect(
                reason="could not authenticate with this token"
            )


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

    log.error("Tried acsess of not authenticated player!")
    return None
