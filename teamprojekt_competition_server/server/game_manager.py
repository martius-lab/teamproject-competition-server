"""Structure which handles multiple games"""

import logging as log
from typing import Type

from .interfaces import IPlayer, IGame


class GameManager:
    """manager for the games"""

    def __init__(self) -> None:
        self.players: list[IPlayer] = []
        self.queue: list[int] = []
        self.games: list[IGame] = []
        self.GameClass: Type[IGame]

    def add_player(self, player: IPlayer) -> None:
        """adds a player to the player list and gives it its index as id

        Args:
            player (IPlayer): player to add
        """
        self.players.append(player)

        player.id = len(self.players) - 1

    def delete_player(self, player_id: int):
        """delete a player from the player array

        Args:
            player_id (int): ID of the player
        """
        self.players.pop(player_id)
        for id in range(player_id, len(self.players)):
            self.players[id].id = id

    def add_player_to_queue(self, player_id: int):
        """adds a player to the queue

        Args:
            player_id (int): id of the player
        """
        if len(self.queue) > 0:
            player1 = self.players[self.queue.pop(0)]
            player2 = self.players[player_id]
            log.debug(f"matched two players: player {player1.id}, player {player2.id}")
            new_game = self.GameClass(players=[player1, player2])
            self.games.append(new_game)
            new_game.start()
        else:
            self.queue.append(player_id)
            log.debug(f"added player to queue. ID: {player_id}")


game_manager = GameManager()
