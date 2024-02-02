from typing import Optional, Type
from queue import Queue
import logging as log

from comprl.server.interfaces import IGame, IPlayer
from comprl.shared.types import GameID, PlayerID


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

    def start_game(self, players: list[IPlayer]) -> GameID:
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

        return game.id

    def end_game(self, game_id: GameID) -> None:
        """
        Ends the game instance with the specified ID.

        Args:
            game_id (GameID): The ID of the game to be ended.
        """
        if game_id in self.games:
            del self.games[game_id]


class PlayerManager:
    """
    Manages connected players.
    """

    def __init__(self) -> None:
        self.players: dict[PlayerID, tuple[IPlayer, bool, int]] = {}

    def add(self, player: IPlayer) -> None:
        """
        Adds a player to the manager.

        Args:
            player (IPlayer): The player object to be added.

        Returns:
            None
        """
        self.players[player.id] = (player, False, -1)

        def __auth(token):
            self.players[player.id][1] = True

        player.authenticate(__auth)

    def remove(self, player: IPlayer) -> None:
        """
        Removes a player from the manager.

        Args:
            player (IPlayer): The player object to be removed.

        Returns:
            None
        """
        if player.id in self.players:
            del self.players[player.id]

    def get_user_id(self, player_id: PlayerID) -> int | None:
        """
        Retrieves the user ID associated with a player.

        Args:
            player_id (PlayerID): The ID of the player.

        Returns:
            Optional[int]: The user ID if found, None otherwise.
        """
        if player_id in self.players:
            return self.players[player_id][2]
        return None

    def get_player_by_id(self, player_id: PlayerID) -> IPlayer | None:
        """
        Retrieves the player object associated with a player ID.

        Args:
            player_id (PlayerID): The ID of the player.

        Returns:
            Optional[IPlayer]: The player object if found, None otherwise.
        """
        if player_id in self.players:
            return self.players[player_id][0]
        return None


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
        if not self.queue.empty():
            players = [
                self.player_manager.get_player_by_id(p_id)
                for p_id in [self.queue.get(), player_id]
            ]

            self.game_manager.start_game(
                [player for player in players if player is not None]
            )

        self.queue.put(player_id)

    def update(self):
        """
        Updates the matchmaking manager.
        """
        pass
