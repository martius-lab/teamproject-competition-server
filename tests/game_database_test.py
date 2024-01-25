import logging
import uuid

import comprl.server.game_database as game_db
from comprl.server.game_result import GameEndState, GameResult

game_db.GAME_DB_FILE = "comprl/server/COMP_database_test.db"

# run with python -m tests.game_database_test

logging.basicConfig(level=logging.DEBUG)


def database_tests():
    gameID1, gameID2, gameID3 = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    game1=GameResult(game_id=gameID1, user1_id=23, user2_id=4, score_user_1=3, score_user_2=6)
    game2=GameResult(game_id=gameID2, user1_id=43, user2_id=23, score_user_1=6, score_user_2=7)
    game3=GameResult(game_id=gameID3, user1_id=1, user2_id=23, score_user_1=6, score_user_2=7, end_state=GameEndState.DISCONNECTED.value)
    game_db.insert_game(game_result=game1)
    game_db.insert_game(game_result=game2)
    game_db.insert_game(game_result=game3)

    assert game_db.get_user_ids(game_id=gameID2) == (43, 23)

    won_games = game_db.get_won_game_ids(user_id=23)
    all_games = game_db.get_game_ids(user_id=23)
    assert len(all_games) % 3 == 0
    assert len(won_games) == len(all_games) / 3
    assert all_games.count(gameID1) == 1
    for game in all_games:
        assert type(game) == uuid.UUID
    for game in won_games:
        assert type(game) == uuid.UUID

    assert game_db.count_played_games(user_id=23) == len(all_games)
    assert game_db.count_won_games(user_id=23) == len(won_games)
    assert game_db.count_disconnected_games(user_id=23) == 0
    assert game_db.count_games_with_disconnect(user_id=23) == len(all_games) / 3
    assert game_db.win_rate(user_id=23) == 0.5


if __name__ == "__main__":
    database_tests()  # only enable for manual testing
    pass
