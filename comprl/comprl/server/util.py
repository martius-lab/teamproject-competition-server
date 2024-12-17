"""
This module contains utility functions for the server.
"""

import uuid

from comprl.shared.types import GameID, PlayerID


class IDGenerator:
    """handles the creation of id's"""

    @staticmethod
    def generate_player_id() -> PlayerID:
        """generates a unique id for players

        Returns:
            PlayerID: obtained id
        """
        return uuid.uuid4()

    @staticmethod
    def generate_game_id() -> GameID:
        """generates a unique id for games

        Returns:
            GameID: obtained id
        """
        return uuid.uuid4()
