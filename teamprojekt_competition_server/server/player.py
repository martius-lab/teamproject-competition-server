"""Player"""

from .protocol import COMPServerProtocol
from .interfaces import IPlayer

from .game_manager import game_manager


class COMPPlayer(IPlayer):
    """player of the game"""

    def __init__(self, connection: COMPServerProtocol) -> None:
        self.connection: COMPServerProtocol = connection
        
        def connected():
            self.authenticate(result_callback=lambda x: game_manager.add_player_to_queue(self.id))
        self.connection.addConnectionMadeCallback(connected)

    def authenticate(self, result_callback):
        return self.connection.get_token(result_callback)

    def notify_start(self):
        self.connection.notify_start()

    def get_action(self, obv, result_callback):
        return self.connection.get_step(obv, result_callback)

    def notify_end(self, result, stats):
        def callback(ready: bool):
            if ready: 
                game_manager.add_player_to_queue(self.id)
        return self.connection.notify_end(result=result, stats=stats, return_callback=callback)
