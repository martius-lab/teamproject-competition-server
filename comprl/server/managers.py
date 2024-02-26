"""
This module contains classes that manage game instances and players.
"""

import logging as log
from typing import Type

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

        log.debug("Game started with players: " + str([p.id for p in players]))

        game.add_finish_callback(self.end_game)
        game.start()

        return game

    def end_game(self, game: IGame) -> None:
        """
        Ends the game instance with the specified ID.

        Args:
            game_id (GameID): The ID of the game to be ended.
        """

        if game.id in self.games:
            game_result = game.get_result()
            if game_result is not None:
                GameData(ConfigProvider.get("game_data")).add(game_result)
            else:
                log.error(f"Game had no valid result. Game-ID: {game.id}")
            del self.games[game.id]

    def force_game_end(self, player_id: PlayerID):
        """Forces all games, that a player is currently playing, to end.

        Args:
            player_id (PlayerID): id of the player
        """
        involved_games: list[IGame] = []
        for _, game in self.games.items():
            for game_player_id in game.players:
                if player_id == game_player_id:
                    involved_games.append(game)
                    break
        for game in involved_games:
            log.debug("Game was forced to end because of a disconnected player")
            game.force_end(player_id=player_id)

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
        player = self.connected_players.get(player_id, None)
        # the player might have disconnected?
        if player is None:
            return False

        id = UserData(ConfigProvider.get("user_data")).get_user_id(token)

        if id is not None:
            # add player to authenticated players
            self.auth_players[player_id] = (self.connected_players[player_id], id)
            # set user_id of player
            player.user_id = id
            log.debug(f"Player {player_id} authenticated")
            return True

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
        This only works for authenticated players.

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

        self.queue: list[PlayerID] = []

    def try_match(self, player_id: PlayerID) -> None:
        """
        Tries to match a player with the given player ID.

        Args:
            player_id (PlayerID): The ID of the player to match.

        Returns:
            None
        """
        player = self.player_manager.get_player_by_id(player_id)

        if player is not None:
            # FIXME: we might wan't to kick the player
            player.is_ready(lambda res: self.match(player_id) if res else None)

    def match(self, player_id: PlayerID) -> None:
        """
        Matches a player with another player from the queue and starts a game.

        Args:
            player_id (PlayerID): The ID of the player to be matched.
        """
        log.debug(f"Player {player_id} is being matched")

        if len(self.queue) > 0:
            players = [
                self.player_manager.get_player_by_id(p_id)
                for p_id in [self.queue.pop(0), player_id]
            ]

            filtered_players = [player for player in players if player is not None]

            game = self.game_manager.start_game(filtered_players)
            game.add_finish_callback(self._end_game)
            return

        self.queue.append(player_id)

    def remove(self, player_id: PlayerID) -> None:
        """
        Removes a player from the matchmaking queue.

        Args:
            player_id (PlayerID): The ID of the player to be removed.
        """
        self.queue = [p for p in self.queue if (p != player_id)]

    def update(self):
        """
        Updates the matchmaking manager.
        """
        pass

    def _end_game(self, game: IGame) -> None:
        """
        Ends the game with the specified ID.

        Args:
            game (IGame): The game to be ended.
        """
        for _, p in game.players.items():
            self.try_match(p.id)
