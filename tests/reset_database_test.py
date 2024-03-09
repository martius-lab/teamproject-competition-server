from comprl.server.data import UserData, GameData
from comprl.server.util import ConfigProvider, IDGenerator
from comprl.server.data.interfaces import GameEndState, GameResult
import comprl.scripts.reset as reset
import logging
import uuid

# run with python -m tests.reset_database_test

logging.basicConfig(level=logging.DEBUG)


def reset_tests():
    user_data = UserData(ConfigProvider.get("user_data"))
    userID1 = user_data.add(
        user_name="user_1",
        user_password=str(uuid.uuid4()),
        user_token=str(uuid.uuid4()),
    )
    userID2 = user_data.add(
        user_name="user_2",
        user_password=str(uuid.uuid4()),
        user_token=str(uuid.uuid4()),
    )
    userID3 = user_data.add(
        user_name="user_3",
        user_password=str(uuid.uuid4()),
        user_token=str(uuid.uuid4()),
    )
    userID4 = user_data.add(
        user_name="user_4",
        user_password=str(uuid.uuid4()),
        user_token=str(uuid.uuid4()),
    )

    user_data.set_matchmaking_parameters(user_id=userID1, mu=24.000, sigma=9.333)
    user_data.set_matchmaking_parameters(user_id=userID2, mu=23.000, sigma=9.000)
    user_data.set_matchmaking_parameters(user_id=userID3, mu=22.000, sigma=7.000)
    user_data.set_matchmaking_parameters(user_id=userID4, mu=21.000, sigma=7.333)

    game_data = GameData(ConfigProvider.get("game_data"))

    gameID1, gameID2, gameID3 = (
        IDGenerator.generate_game_id(),
        IDGenerator.generate_game_id(),
        IDGenerator.generate_game_id(),
    )
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
    game_data.add(game_result=game1)
    game_data.add(game_result=game2)
    game_data.add(game_result=game3)

    # reset
    reset.reset_games(game_data=game_data)
    reset.reset_elo(user_data=user_data)

    (mu, sigma) = user_data.get_matchmaking_parameters(user_id=userID1)
    assert mu == 25.000 and sigma == 8.333

    (mu, sigma) = user_data.get_matchmaking_parameters(user_id=userID2)
    assert mu == 25.000 and sigma == 8.333

    (mu, sigma) = user_data.get_matchmaking_parameters(user_id=userID3)
    assert mu == 25.000 and sigma == 8.333

    (mu, sigma) = user_data.get_matchmaking_parameters(user_id=userID4)
    assert mu == 25.000 and sigma == 8.333

    game_data.cursor.execute(
        f"""SELECT name FROM sqlite_master 
        WHERE type='table' AND name='{game_data.table}'"""
    )
    assert game_data.cursor.fetchone() is None


if __name__ == "__main__":
    # reset_tests()  # only enable for manual testing
    pass
