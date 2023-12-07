"""Structure which handles multiple games"""

import logging as log

from .interfaces import IPlayer, IGame

class GameManager:
    
    players : list[IPlayer] = []
    games : list[IGame] = []
    
    def __init__(self) -> None:
        pass
    
    def add_player(self, player: IPlayer) -> None:
        log.debug("Connected Player")
        
        self.players.append(player)
        