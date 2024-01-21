import uuid

from ..shared.types import GameID, PlayerID

def generate_player_id() -> PlayerID:
    return uuid.uuid4()

def generate_game_id() -> GameID:
    return uuid.uuid4()