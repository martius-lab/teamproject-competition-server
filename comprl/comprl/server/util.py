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


class ConfigProvider:
    """provides configuration settings"""

    __config = {
        "port": 8080,
        "timeout": 10,
        "log_level": "INFO",
        "game_type": None,
        "database_path": None,
        "match_quality_threshold": 0.8,
        "percentage_min_players_waiting": 0.1,
        "percental_time_bonus": 0.1,
    }

    @staticmethod
    def get(key):
        """gets a configuration setting

        Args:
            key (str): key of the setting

        Returns:
            Any: value of the setting
        """
        return ConfigProvider.__config[key]

    @staticmethod
    def set(key, value):
        """sets a configuration setting

        Args:
            key (str): key of the setting
            value (Any): value of the setting
        """
        ConfigProvider.__config[key] = value
