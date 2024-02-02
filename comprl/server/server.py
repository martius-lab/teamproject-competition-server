"""class for server"""

import argparse
import logging as log
import tomllib
import pydoc

from comprl.server.interfaces import IPlayer, IServer
from comprl.server import networking
from comprl.server.managers import GameManager, PlayerManager, MatchmakingManager


class Server(IServer):
    """class for server"""

    def __init__(self):
        self.game_manager = GameManager()
        self.player_manager = PlayerManager()
        self.matchmaking = MatchmakingManager(self.player_manager, self.game_manager)

    def on_start(self):
        """gets called when the server starts"""
        log.info("Starting server")

    def on_stop(self):
        """gets called when the server stops"""
        log.info("Stopping server")

    def on_connect(self, player: IPlayer):
        """gets called when a player connects"""
        log.debug(f"Player {player.id} connected")
        self.player_manager.add(player)

    def on_disconnect(self, player: IPlayer):
        """gets called when a player disconnects"""
        log.debug(f"Player {player.id} disconnected")
        self.player_manager.remove(player)
        
    def on_update(self):
        """gets called every update cycle"""
        self.matchmaking.update()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server arguments")
    parser.add_argument("--config", type=str, help="Config file")
    parser.add_argument("--port", type=int, help="Port to listen on")
    parser.add_argument(
        "--game", type=str, help="File containing the game to run", default="game.py"
    )
    parser.add_argument("--log", type=str, help="Log level", default="INFO")
    args = parser.parse_args()

    if args.config is not None:
        # load config file
        with open(args.config, "rb") as f:
            data = tomllib.load(f)
    else:
        print("No config file provided")

    port = args.port or data["port"] or 65335
    game_type = args.game or data["game"] or "game"
    log_level = args.log or data["log"] or "INFO"

    # set up logging
    log.basicConfig(level=log_level)

    game_type = pydoc.safeimport(game_type)
    if game_type is None:
        raise Exception(f"Could not locate game at {game_type}")

    server = Server()
    networking.launch_server(server, args.port)
