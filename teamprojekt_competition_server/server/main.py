"""run the server"""
from teamprojekt_competition_server.server.server_protocol import COMPServerProtocol
from .server import COMPServer
from .game import AlternatingGame

# run with "python -m teamprojekt_competition_server.server.main"

if __name__ == "__main__":
    
    class MyGame(AlternatingGame):
        def __init__(self, player1: COMPServerProtocol, player2) -> None:
            super().__init__(player1, player2)
            self.env =1
            
        def valid_action(self, action):
            return isinstance(action, int)
        
        def check_game_finished(self) -> bool:
            return (input("Continue game? (y/n)") == "n")
        
        def update_environment(self, action):
            self.env += action["action"]
            print(action, self.env)
    
    server = COMPServer(GameClass=MyGame)
    server.start()
