"""contains matchmaking logic"""

from datetime import datetime
from openskill.models import PlackettLuce
from typing import TypeAlias


from . import game_manager, user_database

from comprl.shared.types import PlayerID

# from .player_manager import get_num_online_players
# TODO fix circular imports

# Type of a player entry in the queue, containing the player ID, user ID, mu, sigma
# and time they joined the queue
QueuePlayer: TypeAlias = tuple[PlayerID, int, float, float, datetime]
# queue storing player id, mu, sigma and time they joined the queue
_queue: list[QueuePlayer] = []
# The model used for matchmaking
model = PlackettLuce()
_MATCH_QUALITY_THRESHOLD = 0.8


def match(player_id: PlayerID, user_id: int) -> None:
    """handles matchmaking between players and starts the game

    Args:
        id (PlayerID): id of the player to match
        user_ID (int): user id of the player
        mu (float): current mu value of the player
        sigma (float): current sigma value of the player
    """

    mu, sigma = user_database.get_matchmaking_parameters(user_id)

    # check if enough players are waiting
    if len(_queue) < _min_players_waiting():
        _queue.append((player_id, user_id, mu, sigma, datetime.now()))
        return
    else:
        now = datetime.now()
        for player2 in _queue:
            player1 = player_id, user_id, mu, sigma, now
            # try matching the new player against all players in the queue
            if _try_matching(player1, player2):
                return
        # no suitable match found
        _queue.append((player_id, user_id, mu, sigma, datetime.now()))
        return


def _min_players_waiting() -> int:
    """calculates how many players at minimum need to wait in the queue"""
    active_players = 0  # TODO get_num_online_players()
    return int(max(1, active_players * 0.1))


def _rate_match_quality(
    mu_p1, sigma_p1, time_stamp_p1, mu_p2, sigma_p2, time_stamp_p2
) -> float:
    """returns the expected fairness of the game, considering the waiting time of both
    players."""
    now = datetime.now()
    waiting_time_p1 = (time_stamp_p1 - now).total_seconds()
    waiting_time_p2 = (time_stamp_p2 - now).total_seconds()
    combined_waiting_time = waiting_time_p1 + waiting_time_p2
    # calculate a bonus if the players waited a long time
    waiting_bonus = max(0.0, (combined_waiting_time / 60 - 1) * 0.1)
    # TODO play with this function. Maybe even use polynomial or exponential growth,
    # depending on waiting time

    p1 = model.create_rating([mu_p1, sigma_p1], "player1")
    p2 = model.create_rating([mu_p2, sigma_p2], "player2")
    draw_prob = model.predict_draw([[p1], [p2]])
    return draw_prob + waiting_bonus


def _try_matching(player1: QueuePlayer, player2: QueuePlayer) -> bool:
    """try matching the given two players, if their match quality is above the
    threshold. If successful, the players are removed from the queue, a game is
    started and True is returned. Otherwise False is returned.

    Args:
        player1 (_type_): args of the first player
        player2 (_type_): args of the second player

    Returns:
        bool: wether the players were matched
    """
    player1_id, user1_id, mu_p1, sigma_p1, time_stamp_p1 = player1
    player2_id, user2_id, mu_p2, sigma_p2, time_stamp_p2 = player2
    match_quality = _rate_match_quality(
        mu_p1, sigma_p1, time_stamp_p1, mu_p2, sigma_p2, time_stamp_p2
    )
    # prevent the user from playing against himself
    if user1_id == user2_id:
        return False

    if match_quality > _MATCH_QUALITY_THRESHOLD:
        # match the players. We could search for best match but using the first adds a
        # bit of diversity and the players in front of the queue are waiting longer,
        # so its fairer for them.

        # remove p2 from queue and match p1 and p2
        _queue.remove(player2)
        game_manager.start_game([player2_id, player1_id])
        return True
    return False


def update() -> None:
    """update the current queue and tries to match waiting players"""
    for i in range(len(_queue)):
        for j in range(i, len(_queue)):
            # try to match all players against each other
            if _try_matching(_queue[i], _queue[j]):
                return
    return
