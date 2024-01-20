import uuid

from ..shared.types import game_id, player_id

def generate_player_id() -> player_id:
    return uuid.uuid4()

def generate_game_id() -> game_id:
    return uuid.uuid4()