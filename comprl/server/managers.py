"""
This module contains classes that manage game instances and players.
"""

import logging as log
from typing import Type
from queue import Queue

from comprl.server.interfaces import IGame, IPlayer
from comprl.shared.types import GameID, PlayerID
from comprl.server.data import GameData, UserData
from comprl.server.util import ConfigProvider


class GameManager:
    """
    A class that manages game instances of a specific game type.

    Attributes:
        games (dict[GameID, IGame]): A dictionary that stores active game instances.
        game_type (Type[IGame]): The type of game to be managed.
    """

    def __init__(self, game_type: Type[IGame]) -> None:
        self.games: dict[GameID, IGame] = {}
        self.game_type = game_type

    def start_game(self, players: list[IPlayer]) -> IGame:
        """
        Starts a new game instance with the given players.

        Args:
            players (list[IPlayer]): A list of players participating in the game.

        Returns:
            GameID: The ID of the newly started game.
        """
        game = self.game_type(players)
        self.games[game.id] = game

        game.add_finish_callback(self.end_game)
        game.start()

        return game

    def end_game(self, game_id: GameID) -> None:
        """
        Ends the game instance with the specified ID.

        Args:
            game_id (GameID): The ID of the game to be ended.
        """

        if game_id in self.games:

            GameData(ConfigProvider.get("game_data")).add(
                self.games[game_id].get_result()
            )

            del self.games[game_id]

    def get(self, game_id: GameID) -> IGame | None:
        """
        Retrieves the game instance with the specified ID.

        Args:
            game_id (GameID): The ID of the game to be retrieved.

        Returns:
            Optional[IGame]: The game instance if found, None otherwise.
        """
        return self.games.get(game_id, None)


class PlayerManager:
    """
    Manages connected players.
    """

    def __init__(self) -> None:
        self.auth_players: dict[PlayerID, tuple[IPlayer, int]] = {}
        self.connected_players: dict[PlayerID, IPlayer] = {}

    def add(self, player: IPlayer) -> None:
        """
        Adds a player to the manager.

        Args:
            player (IPlayer): The player object to be added.

        Returns:
            None
        """
        self.connected_players[player.id] = player

    def auth(self, player_id: PlayerID, token: str) -> bool:
        """
        Authenticates a player using their player ID and token.

        Args:
            player_id (PlayerID): The ID of the player.
            token (str): The authentication token.

        Returns:
            bool: True if the authentication is successful, False otherwise.
        """

        data = UserData(ConfigProvider.get("user_data"))
        if data.is_verified(token):
            self.auth_players[player_id] = (
                self.connected_players[player_id],
                data.get_user_id(token),
            )
            log.info(f"Player {player_id} authenticated")
            return True
        # disconnect player if authentication failed
        self.connected_players[player_id].disconnect("Authentication failed")

        return False

    def remove(self, player: IPlayer) -> None:
        """
        Removes a player from the manager.

        Args:
            player (IPlayer): The player object to be removed.

        Returns:
            None
        """
        if player.id in self.connected_players:
            del self.connected_players[player.id]

            if player.id in self.auth_players:
                del self.auth_players[player.id]

    def get_user_id(self, player_id: PlayerID) -> int | None:
        """
        Retrieves the user ID associated with a player.

        Args:
            player_id (PlayerID): The ID of the player.

        Returns:
            Optional[int]: The user ID if found, None otherwise.
        """
        if player_id in self.auth_players:
            return self.auth_players[player_id][1]
        return None

    def get_player_by_id(self, player_id: PlayerID) -> IPlayer | None:
        """
        Retrieves the player object associated with a player ID.

        Args:
            player_id (PlayerID): The ID of the player.

        Returns:
            Optional[IPlayer]: The player object if found, None otherwise.
        """
        if player_id in self.auth_players:
            return self.auth_players[player_id][0]
        return None

    def broadcast_error(self, msg: str) -> None:
        """
        Broadcasts a message to all connected players.

        Args:
            msg (str): The message to be broadcasted.

        Returns:
            None
        """

        for player in self.connected_players.values():
            player.notify_error(msg)

    def broadcast_error_auth(self, msg: str) -> None:
        """
        Broadcasts a message to all authenticated players.

        Args:
            msg (str): The message to be broadcasted.

        Returns:
            None
        """

        for player, _ in self.auth_players.values():
            player.notify_error(msg)

    def disconnect_all(self, reason: str) -> None:
        """
        Disconnects all connected players.

        Args:
            reason (str): The reason for disconnection.

        Returns:
            None
        """

        for player in self.connected_players.values():
            player.disconnect(reason)


class MatchmakingManager:
    """handles matchmaking between players and starts the game"""

    def __init__(
        self, player_manager: PlayerManager, game_manager: GameManager
    ) -> None:
        """
        Initializes a MatchmakingManager object.

        Args:
            player_manager (PlayerManager): The player manager object.
            game_manager (GameManager): The game manager object.
        """
        self.player_manager = player_manager
        self.game_manager = game_manager

        self.queue: Queue[PlayerID] = Queue()

    def match(self, player_id: PlayerID) -> None:
        """
        Matches a player with another player from the queue and starts a game.

        Args:
            player_id (PlayerID): The ID of the player to be matched.
        """
        log.debug(f"Player {player_id} is being matched")

        if not self.queue.empty():
            players = [
                self.player_manager.get_player_by_id(p_id)
                for p_id in [self.queue.get(), player_id]
            ]

            filtered_players = [player for player in players if player is not None]

            self.game_manager.start_game(filtered_players)

            # TODO: requeue players if the game ended

        self.queue.put(player_id)

    def remove(self, player_id: PlayerID) -> None:
        """
        Removes a player from the matchmaking queue.

        Args:
            player_id (PlayerID): The ID of the player to be removed.
        """
        pass

    def update(self):
        """
        Updates the matchmaking manager.
        """
        pass
