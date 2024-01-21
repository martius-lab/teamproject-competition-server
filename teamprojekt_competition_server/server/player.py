"""Player"""

from .protocol import COMPServerProtocol
from .interfaces import IPlayer

from . import player_manager


class COMPPlayer(IPlayer):
    """player of the game"""

    def __init__(self, connection: COMPServerProtocol):
        #init super to obtain id
        super().__init__()
        
        #set the networing connection
        self.connection: COMPServerProtocol = connection
        
        def __auth():
            """Connects player to server"""
            self.authenticate(
                result_callback=lambda token: player_manager.authenticate(self.id ,token) 
            )
        
        #when connection made we want to authenticate
        self.connection.addConnectionMadeCallback(__auth) #add the callback for authentication
        
        #if we lose connection we also need to notify the manager
        self.connection.addConnectionLostCallback(lambda : player_manager.remove(self.id)) #add the callback for loosing the connection

    def authenticate(self, result_callback):
        """authenticates player

        Args: resul_callback (callback function)

        Returns: token (string)"""
        return self.connection.get_token(result_callback)

    def notify_start(self):
        """notifies start of game"""
        self.connection.notify_start()

    def get_action(self, obv, result_callback):
        """receive action from server

        Args:
            obv(any): observation"""
        return self.connection.get_step(obv, result_callback)

    def notify_end(self, result, stats):
        """called when game ends

        Args:
            result (any): result of the game
            stats: (any): stats of the game"""

        def callback(ready: bool):
            if ready:
                pass

        return self.connection.notify_end(
            result=result, stats=stats, return_callback=callback
        )
