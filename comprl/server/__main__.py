"""
class for server
"""

import os
import argparse
import logging as log

try:
    import tomllib  # type: ignore[import-not-found]
except ImportError:
    # tomllib was added in Python 3.11.  Older versions can use tomli
    import tomli as tomllib  # type: ignore[import-not-found, no-redef]

import importlib.util
import importlib.abc

from comprl.server import networking
from comprl.server.managers import GameManager, PlayerManager, MatchmakingManager
from comprl.server.interfaces import IPlayer, IServer
from comprl.server.util import ConfigProvider
from comprl.server.data import ConnectionInfo


class Server(IServer):
    """class for server"""

    def __init__(self):
        self.game_manager = GameManager(ConfigProvider.get("game_type"))
        self.player_manager = PlayerManager()
        self.matchmaking = MatchmakingManager(self.player_manager, self.game_manager)

    def on_start(self):
        """gets called when the server starts"""
        log.info("Server started")

    def on_stop(self):
        """gets called when the server stops"""
        log.info("Server stopped")

    def on_connect(self, player: IPlayer):
        """gets called when a player connects"""
        log.debug(f"Player {player.id} connected")
        self.player_manager.add(player)

        def __auth(token):
            if self.player_manager.auth(player.id, token):
                self.matchmaking.try_match(player.id)
            else:
                player.disconnect("Authentication failed")

        player.authenticate(__auth)

    def on_disconnect(self, player: IPlayer):
        """gets called when a player disconnects"""
        log.debug(f"Player {player.id} disconnected")
        self.matchmaking.remove(player.id)
        self.player_manager.remove(player)
        self.game_manager.force_game_end(player.id)

    def on_timeout(self, player: IPlayer, failure, timeout):
        """gets called when a player has a timeout"""
        log.debug(f"Player {player.id} had timeout after {timeout}s")
        player.disconnect(reason=f"Timeout after {timeout}s")

    def on_update(self):
        """gets called every update cycle"""
        self.matchmaking.update()


def load_class(module_path: str, class_name: str):
    """
    Loads a a class from a module.
    """
    # get the module name by splitting the path and removing the file extension
    name = module_path.split(os.sep)[-1].split(".")[0]

    # load the module
    spec = importlib.util.spec_from_file_location(name, module_path)

    # check if the module could be loaded
    if spec is None:
        return None

    # create the module
    module = importlib.util.module_from_spec(spec)

    # this is for mypy
    if not isinstance(spec.loader, importlib.abc.Loader):
        return None

    # exec the module
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError:
        return None

    # finally get the class
    return getattr(module, class_name)


def main():
    """
    Main function to start the server.
    """
    parser = argparse.ArgumentParser(
        description="The following arguments are supported:"
    )
    parser.add_argument("--config", type=str, help="Config file")
    parser.add_argument("--port", type=int, help="Port to listen on")
    parser.add_argument(
        "--timeout", type=int, help="Seconds to wait for a player to answer"
    )
    parser.add_argument("--game_path", type=str, help="File containing the game to run")
    parser.add_argument("--game_class", type=str, help="Classname of the game")
    parser.add_argument("--log", type=str, help="Log level")
    parser.add_argument(
        "--game_db_path",
        type=str,
        help="Path to the database file (doesn't have to exist)",
    )
    parser.add_argument(
        "--game_db_name", type=str, help="Name of the game table in the file"
    )
    parser.add_argument("--user_db_path", type=str, help="Path to the database file")
    parser.add_argument(
        "--user_db_name", type=str, help="Name of the user table in the file"
    )
    args = parser.parse_args()

    data = None
    if args.config is not None:
        # load config file
        with open(args.config, "rb") as f:
            data = tomllib.load(f)["CompetitionServer"]
    else:
        print("No config file provided, using arguments or defaults")

    port = args.port or data["port"] if data else 65335
    timeout = args.timeout or data["timeout"] if data else 10
    game_path = args.game_path or data["game_path"] if data else "game.py"
    game_class = args.game_class or data["game_class"] if data else "Game"
    log_level = args.log or data["log"] if data else "INFO"
    game_db_path = args.game_db_path or data["game_db_path"] if data else "games.db"
    game_db_name = args.game_db_name or data["game_db_name"] if data else "game_data"
    user_db_path = args.user_db_path or data["user_db_path"] if data else "users.db"
    user_db_name = args.user_db_name or data["user_db_name"] if data else "user_data"

    # set up logging
    log.basicConfig(level=log_level)

    # get working directory
    full_path = os.path.join(os.getcwd(), game_path)

    # try to load the game class
    game_type = load_class(full_path, game_class)
    # check if the class could be loaded
    if game_type is None:
        log.error(f"Could not load game class from {full_path}")
        return

    # write the config to the ConfigProvider
    ConfigProvider.set("port", port)
    ConfigProvider.set("timeout", timeout)
    ConfigProvider.set("log_level", log_level)
    ConfigProvider.set("game_type", game_type)
    ConfigProvider.set("game_data", ConnectionInfo(game_db_path, game_db_name))
    ConfigProvider.set("user_data", ConnectionInfo(user_db_path, user_db_name))

    server = Server()
    networking.launch_server(server, port)


if __name__ == "__main__":
    main()
