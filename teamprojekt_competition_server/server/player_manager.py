import logging as log
import uuid

from .interfaces import IPlayer, player_id

_connected_players: dict[player_id, IPlayer] = {}
_authenticated_players: dict[player_id, IPlayer] = {}

def register(player: IPlayer) -> player_id:
    _connected_players[player.id] = player
    log.debug(f"Player registered with id:{player.id}")


def authenticate(id : player_id, token: str) -> None:
    log.debug(f"Player registered with id:{id} authenticated with token:{token}")
    if id in _connected_players:
        _authenticated_players[id] = True
        
def remove(id: player_id):
    if id in _connected_players:
        log.debug(f"Player with id:{id} disconnected")
        del _connected_players[id]
    
    if id in _authenticated_players:
        del _authenticated_players[id]