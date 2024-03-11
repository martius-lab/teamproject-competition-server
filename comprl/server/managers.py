"""
This module contains classes that manage game instances and players.
"""

import logging as log
from typing import Type
from datetime import datetime
from openskill.models import PlackettLuce
from typing import TypeAlias

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

    def get_matchmaking_parameters(self, user_id: int) -> tuple[float, float]:
        """
        Retrieves the matchmaking parameters of a user based on their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            tuple[float, float]: The mu and sigma values of the user.
        """
        return UserData(ConfigProvider.get("user_data")).get_matchmaking_parameters(
            user_id
        )

    def update_matchmaking_parameters(
        self, user_id: int, new_mu: float, new_sigma: float
    ) -> None:
        """
        Updates the matchmaking parameters of a user based on their ID.

        Args:
            user_id (int): The ID of the user.
            new_mu (float): The new mu value of the user.
            new_sigma (float): The new sigma value of the user.
        """
        UserData(ConfigProvider.get("user_data")).set_matchmaking_parameters(
            user_id, new_mu, new_sigma
        )


# Type of a player entry in the queue, containing the player ID, user ID, mu, sigma
# and time they joined the queue
QueuePlayer: TypeAlias = tuple[PlayerID, int, float, float, datetime]


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

        # queue storing player id, mu, sigma and time they joined the queue
        self._queue: list[QueuePlayer] = []
        # The model used for matchmaking
        self.model = PlackettLuce()
        self._MATCH_QUALITY_THRESHOLD = 0.8
        self._PERCENTAGE_MIN_PLAYERS_WAITING = 0.1

    def try_match(self, player_id: PlayerID) -> None:
        """
        Tries to add a player with the given player ID to the matchmaking queue.

        Args:
            player_id (PlayerID): The ID of the player to match.

        Returns:
            None
        """
        player = self.player_manager.get_player_by_id(player_id)
        if player is not None:
            # FIXME: we might wan't to kick the player

            def __match(ready: bool):
                if ready:
                    player.notify_info(msg="Waiting in queue")
                    self.match(player_id)

            player.is_ready(result_callback=__match)

    def match(self, player_id: PlayerID) -> None:
        """
        Adds player to the queue.

        Args:
            player_id (PlayerID): The ID of the player to be matched.
        """
        user_id = self.player_manager.get_user_id(player_id)
        if user_id is None:
            log.error(f"Player {player_id} is not authenticated but tried to queue.")
            return
        mu, sigma = self.player_manager.get_matchmaking_parameters(user_id)

        # check if enough players are waiting
        self._queue.append((player_id, user_id, mu, sigma, datetime.now()))

        log.debug(f"Player {player_id} was added to the queue")

        return

    def remove(self, player_id: PlayerID) -> None:
        """
        Removes a player from the matchmaking queue.

        Args:
            player_id (PlayerID): The ID of the player to be removed.
        """
        self._queue = [
            (p_id, u_id, mu, sigma, time)
            for p_id, u_id, mu, sigma, time in self._queue
            if (p_id != player_id)
        ]

    def _update(self, start_index: int = 0) -> None:
        """
        Updates the matchmaking manager.

        start_index (int, optional): The position in queue to start matching from.
        Used for recursion. Defaults to 0.
        """

        if len(self._queue) < self._min_players_waiting():
            return

        for i in range(start_index, len(self._queue)):
            for j in range(i + 1, len(self._queue)):
                # try to match all players against each other
                if self._try_start_game(self._queue[i], self._queue[j]):
                    # players are matched and removed from queue. continue searching
                    self._update(i)
        return

    def _min_players_waiting(self) -> int:
        """
        Returns the minimum number of players that need to be waiting in the queue.

        Returns:
            int: The minimum number of players.
        """
        return int(
            len(self.player_manager.auth_players) * self._PERCENTAGE_MIN_PLAYERS_WAITING
        )

    def _try_start_game(self, player1: QueuePlayer, player2: QueuePlayer) -> bool:
        """
        Tries to start a game with the given players.

        Args:
            player1 (QueuePlayer): The first player.
            player2 (QueuePlayer): The second player.

        Returns:
            bool: True if the game was started, False otherwise.
        """
        player1_id, user1_id, _, _, _ = player1
        player2_id, user2_id, _, _, _ = player2
        match_quality = self._rate_match_quality(player1, player2)
        # prevent the user from playing against himself
        if user1_id == user2_id:
            return False

        if match_quality > self._MATCH_QUALITY_THRESHOLD:
            # match the players. We could search for best match but using the first adds
            # a bit of diversity and the players in front of the queue are waiting
            # longer, so its fairer for them.

            players = [
                self.player_manager.get_player_by_id(player1_id),
                self.player_manager.get_player_by_id(player2_id),
            ]

            filtered_players = [player for player in players if player is not None]

            if len(filtered_players) != 2:
                log.error("Player was in queue but not in player manager")
                if players[0] is None:
                    self.remove(player1_id)
                if players[1] is None:
                    self.remove(player2_id)
                return False

            self.remove(player1_id)
            self.remove(player2_id)

            game = self.game_manager.start_game(filtered_players)
            game.add_finish_callback(self._end_game)
            return True
        return False

    def _rate_match_quality(self, player1: QueuePlayer, player2: QueuePlayer) -> float:
        """
        Rates the match quality between two players.

        Args:
            player1 (QueuePlayer): The first player.
            player2 (QueuePlayer): The second player.

        Returns:
            float: The match quality.
        """
        _, _, mu_p1, sigma_p1, time_stamp_p1 = player1
        _, _, mu_p2, sigma_p2, time_stamp_p2 = player2
        now = datetime.now()
        waiting_time_p1 = (now - time_stamp_p1).total_seconds()
        waiting_time_p2 = (now - time_stamp_p2).total_seconds()
        combined_waiting_time = waiting_time_p1 + waiting_time_p2
        # calculate a bonus if the players waited a long time
        waiting_bonus = max(0.0, (combined_waiting_time / 60 - 1) * 0.1)
        # TODO play with this function. Maybe even use polynomial or exponential growth,
        # depending on waiting time

        rating_p1 = self.model.create_rating([mu_p1, sigma_p1], "player1")
        rating_p2 = self.model.create_rating([mu_p2, sigma_p2], "player2")
        draw_prob = self.model.predict_draw([[rating_p1], [rating_p2]])
        return draw_prob + waiting_bonus

    def _end_game(self, game: IGame) -> None:
        """
        Readds players to queue after game has ended.

        Args:
            game (IGame): The game to be ended.
        """
        # update elo values
        result = game.get_result()
        if result is not None:
            mu_p1, sigma_p1 = self.player_manager.get_matchmaking_parameters(
                result.user1_id
            )
            mu_p2, sigma_p2 = self.player_manager.get_matchmaking_parameters(
                result.user2_id
            )
            rating_p1 = self.model.create_rating([mu_p1, sigma_p1], "player1")
            rating_p2 = self.model.create_rating([mu_p2, sigma_p2], "player2")
            [[p1], [p2]] = self.model.rate(
                [[rating_p1], [rating_p2]],
                scores=[result.score_user_1, result.score_user_2],
            )
            self.player_manager.update_matchmaking_parameters(
                result.user1_id, p1.mu, p1.sigma
            )
            self.player_manager.update_matchmaking_parameters(
                result.user2_id, p2.mu, p2.sigma
            )

        for _, p in game.players.items():
            self.try_match(p.id)
