"""Structure which handles multiple games"""

import io
from twisted.logger import Logger, textFileLogObserver
from typing import Type
from .interfaces import IPlayer, IGame


class GameManager:
    log = Logger(observer=textFileLogObserver(io.open("./teamprojekt_competition_server/log/server/gameManager.log", "a")))

    def __init__(self) -> None:
        self.players: list[IPlayer] = []
        self.queue: list[int] = []
        self.games: list[IGame] = []
        self.GameClass: Type[IGame]
        self.log.info("Initialized GameManager -> {}".format(id(self)))

    def add_player(self, player: IPlayer) -> None:
        self.players.append(player)
        player.id = len(self.players)-1
        self.log.info("\t\tAdded player with id: {}".format(player.id))
    
    def add_player_to_queue(self, player_id: int):
        if len(self.queue) > 0:
            player1 = self.players[self.queue.pop(0)]
            player2 = self.players[player_id]
            print(f"[GamerManager]: matched two players: player1 {player1.id}, player2 {player2.id}")
            self.log.info("\t\tMatched two players: player1 {}, player2 {}".format(player1.id, player2.id))

            new_game = self.GameClass(players=[player1, player2])
            self.games.append(new_game)
            new_game.start()
            self.log.info("\t\tStarted game: {}".format(id(new_game)))

        else:
            self.queue.append(player_id)
            print(f"added player to queue. ID: {player_id}")
            self.log.info("added player with id: {} to queue".format(player_id))

game_manager = GameManager()
