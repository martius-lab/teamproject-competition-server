"""Structure which handles multiple games"""

import logging as log
from typing import Type

from .interfaces import IPlayer, IGame


class GameManager:
    
    def __init__(self) -> None:
        self.players: list[IPlayer] = []
        self.queue: list[int] = []
        self.games: list[IGame] = []
        self.GameClass: Type[IGame]

    def add_player(self, player: IPlayer) -> None:
        self.players.append(player)
        
        player.id = len(self.players)-1
    
    def add_player_to_queue(self, player_id: int):
        if len(self.queue) > 0:
            player1 = self.players[self.queue.pop(0)]
            player2 = self.players[player_id]
            log.debug(f"matched two players: player1 {player1.id}, player2 {player2.id}")
            new_game = self.GameClass(players=[player1, player2])
            self.games.append(new_game)
            new_game.start()
        else:
            self.queue.append(player_id)
            log.debug(f"added player to queue. ID: {player_id}")

game_manager = GameManager()