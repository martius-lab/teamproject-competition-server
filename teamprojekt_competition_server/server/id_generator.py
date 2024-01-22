"""handles the creation of id's"""
import uuid

from ..shared.types import GameID, PlayerID


def generate_player_id() -> PlayerID:
    """generates a unique id for players

    Returns:
        PlayerID: obtained id
    """
    return uuid.uuid4()


def generate_game_id() -> GameID:
    """generates a unique id for games

    Returns:
        GameID: obtained id
    """
    return uuid.uuid4()
