"""Player"""

from .protocol import COMPServerProtocol
from .interfaces import IPlayer

from .game_manager import game_manager


class COMPPlayer(IPlayer):
    """player of the game"""

    def __init__(self, connection: COMPServerProtocol) -> None:
        self.connection: COMPServerProtocol = connection

        def connected():
            """Connects player to server"""
            self.authenticate(
                result_callback=lambda x: game_manager.add_player_to_queue(self.id)
            )

        def disconnected():
            """remove the player from the game manager"""
            game_manager.delete_player(player_id=self.id)

        self.connection.addConnectionMadeCallback(connected)
        self.connection.addConnectionLostCallback(disconnected)

    def authenticate(self, result_callback):
        """authenticates player

        Args: result_callback (callback function)

        Returns: token (string)"""
        self.connection.get_token(result_callback)

    def notify_start(self, game_id: int):
        """notifies start of game"""
        self.connection.notify_start(game_id=game_id)

    def get_action(self, obv, result_callback):
        """receive action from server

        Args:
            obv(any): observation"""
        self.connection.get_step(obv, result_callback)

    def notify_end(self, result, stats):
        """called when game ends

        Args:
            result (any): result of the game
            stats: (any): stats of the game"""

        def callback(ready: bool):
            if ready:
                game_manager.add_player_to_queue(self.id)

        return self.connection.notify_end(
            result=result, stats=stats, return_callback=callback
        )
