"""Structure which handles multiple games"""

import logging as log
from typing import Type

from .interfaces import IPlayer, IGame


class GameManager:
    players: list[IPlayer] = []
    queue: list[int] = []
    games: list[IGame] = []
    GameClass: Type[IGame]

    def __init__(self) -> None:
        pass

    def add_player(self, player: IPlayer) -> None:
        self.players.append(player)
        log.debug("Player added")
        
        player.id = len(self.players)-1
    
    def add_player_to_queue(self, player_id: int):
        if len(self.queue) > 0:
            log.debug("matched two players")
            player1 = self.players[self.queue.pop()]
            player2 = self.players[player_id]
            new_game = self.GameClass(players=[player1, player2])
            self.games.append(new_game)
            new_game.start()
        else:
            self.queue.append(player_id)
            log.debug("added player to queue")


game_manager = GameManager()