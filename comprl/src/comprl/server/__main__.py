"""Run the comprl server."""

from __future__ import annotations

import argparse
import importlib.abc
import importlib.util
import inspect
import logging as log
import os
import pathlib
from typing import Type, TYPE_CHECKING

from comprl.server import config, networking
from comprl.server.managers import GameManager, PlayerManager, MatchmakingManager
from comprl.server.interfaces import IPlayer, IServer

if TYPE_CHECKING:
    from comprl.server.interfaces import IGame


class Server(IServer):
    """class for server"""

    def __init__(self, game_type: Type[IGame]):
        self.game_manager = GameManager(game_type)
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
                player.notify_info(msg="Authentication successful")
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

    def on_remote_error(self, player: IPlayer, error: Exception):
        """gets called when there is an error in deferred"""
        if player.is_connected:
            log.error(f"Connected player caused remote error \n {error}")
        else:
            log.debug("Disconnected player caused remote error")

    def on_update(self):
        """gets called every update cycle"""
        self.matchmaking._update()


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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=pathlib.Path, help="Config file")
    parser.add_argument("--config-overwrites", type=str, nargs="+", default=[])
    args = parser.parse_args()

    try:
        conf = config.load_config(args.config, args.config_overwrites)
    except Exception as e:
        log.error("Failed to load config: %s", e)
        return

    # set up logging
    log.basicConfig(level=conf.log_level)

    # resolve relative game_path w.r.t. current working directory
    absolute_game_path = os.path.join(os.getcwd(), conf.game_path)

    # try to load the game class
    game_type = load_class(absolute_game_path, conf.game_class)
    # check if the class could be loaded
    if game_type is None:
        log.error(f"Could not load game class from {absolute_game_path}")
        return
    # check if the class is fully implemented
    if inspect.isabstract(game_type):
        log.error("Provided game class is not valid because it is still abstract.")
        return

    if not conf.data_dir.is_dir():
        log.error("data_dir '%s' not found or not a directory", conf.data_dir)
        return

    server = Server(game_type)
    networking.launch_server(
        server=server, port=conf.port, update_interval=conf.server_update_interval
    )


if __name__ == "__main__":
    main()
