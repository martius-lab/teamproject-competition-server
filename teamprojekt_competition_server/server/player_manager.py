import logging as log
import uuid

from .interfaces import IPlayer

class PlayerId(uuid.UUID):
    pass

_connected_players: dict[PlayerId, IPlayer] = {}
_authenticated_players: dict[PlayerId, IPlayer] = {}

def register(player: IPlayer) -> PlayerId:
    player_id = uuid.uuid4()
    log.debug(f"Player registered with id:{player_id}")
    _connected_players[player_id] = player
    return player_id


def authenticate(id : PlayerId, token: str) -> None:
    log.debug(f"Player registered with id:{id} authenticated with token:{token}")
    if id in _connected_players:
        _authenticated_players[id] = True
        
def remove(id: PlayerId):
    if id in _connected_players:
        log.debug(f"Player with id:{id} disconnected")
        del _connected_players[id]
    
    if id in _authenticated_players:
        del _authenticated_players[id]