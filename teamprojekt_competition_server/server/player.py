"""Player"""

from .protocol import COMPServerProtocol
from .interfaces import IPlayer

from .game_manager import game_manager


class COMPPlayer(IPlayer):
    connection: COMPServerProtocol

    def __init__(self, connection: COMPServerProtocol) -> None:
        self.connection = connection
        
        def connection_made():
            self.authenticate(result_callback=lambda x: game_manager.add_player_to_queue(self.id))
        self.connection.addConnectionMadeCallback(connection_made)

    def authenticate(self, result_callback):
        return self.connection.get_token(result_callback)

    def notify_start(self):
        self.connection.notify_start()

    def get_action(self, obv, result_callback):
        return self.connection.get_step(obv, result_callback)

    def notify_end(self):
        return self.connection.notify_end()
