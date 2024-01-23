"""contains matchmaking logic"""

from queue import Queue

from . import game_manager

from teamprojekt_competition_server.shared.types import PlayerID

_queue: Queue[PlayerID] = Queue()


def match(id: PlayerID) -> None:
    """handles mathcmaking between players and starts the game

    Args:
        id (PlayerID): id of the player to match
    """
    # some simple quick and dirty "matchmaking"
    if not _queue.empty():
        game_manager.start_game([_queue.get(), id])
        return

    _queue.put(id)
