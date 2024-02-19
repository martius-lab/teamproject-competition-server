import comprl.server.user_database as user_db
import comprl.server.game_database as game_db
from comprl.server.game_result import GameEndState, GameResult
import comprl.scripts.reset as reset
import sqlite3
import logging
import uuid

# run with python -m tests.reset_database_test

logging.basicConfig(level=logging.DEBUG)


def reset_tests():
    tokens = [uuid.uuid4() for _ in range(4)]
    userID1 = user_db.add_user(user_name="user_1", user_token=tokens[0])
    userID2 = user_db.add_user(user_name="user_2", user_token=tokens[1])
    userID3 = user_db.add_user(user_name="user_3", user_token=tokens[2])
    userID4 = user_db.add_user(user_name="user_4", user_token=tokens[3])

    user_db.update_matchmaking_parameters(id=userID1, new_mu=24.000, new_sigma=9.333)
    user_db.update_matchmaking_parameters(id=userID2, new_mu=23.000, new_sigma=9.000)
    user_db.update_matchmaking_parameters(id=userID3, new_mu=22.000, new_sigma=7.000)
    user_db.update_matchmaking_parameters(id=userID4, new_mu=21.000, new_sigma=7.333)

    gameID1, gameID2, gameID3 = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    game1 = GameResult(
        game_id=gameID1, user1_id=23, user2_id=4, score_user_1=3, score_user_2=6
    )
    game2 = GameResult(
        game_id=gameID2, user1_id=43, user2_id=23, score_user_1=6, score_user_2=7
    )
    game3 = GameResult(
        game_id=gameID3,
        user1_id=1,
        user2_id=23,
        score_user_1=6,
        score_user_2=7,
        end_state=GameEndState.DISCONNECTED.value,
    )
    game_db.insert_game(game_result=game1)
    game_db.insert_game(game_result=game2)
    game_db.insert_game(game_result=game3)

    # reset
    reset.reset_games()
    reset.reset_elo()

    (mu, sigma) = user_db.get_matchmaking_parameters(id=userID1)
    assert mu == 25.000 and sigma == 8.333

    (mu, sigma) = user_db.get_matchmaking_parameters(id=userID2)
    assert mu == 25.000 and sigma == 8.333

    (mu, sigma) = user_db.get_matchmaking_parameters(id=userID3)
    assert mu == 25.000 and sigma == 8.333

    (mu, sigma) = user_db.get_matchmaking_parameters(id=userID4)
    assert mu == 25.000 and sigma == 8.333

    GAME_DB_NAME = "game"
    GAME_DB_FILE = "comprl/server/COMP_database.db"
    connection = sqlite3.connect(GAME_DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        f"""SELECT name FROM sqlite_master 
        WHERE type='table' AND name='{GAME_DB_NAME}'"""
    )
    assert cursor.fetchone() is None

    connection.close()


if __name__ == "__main__":
    # reset_tests()  # only enable for manual testing
    pass
